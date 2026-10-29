"""Pull fresh COROS data into plans/jayesh-snapshot.json.

Run with the coros-mcp virtualenv so `coros_mcp` is importable:

    ~/Repos/coros/.venv/bin/python scripts/update_from_coros.py

Exit codes: 0 = snapshot written, 2 = no usable COROS login (run `coros-mcp auth-web`).
Only reads from COROS; never touches the training calendar.
"""
import asyncio
import datetime as dt
import json
import os
import sys

from coros_mcp import coros_api

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = os.path.join(ROOT, "plans", "jayesh-345.json")
OUT = os.path.join(ROOT, "plans", "jayesh-snapshot.json")
RUN_SPORTS = {100, 101, 102, 103}  # road, indoor, trail, track
DONE_SHARE = 0.5  # a planned run counts as done if at least half its distance was run that day


async def get_auth():
    auth = coros_api.get_stored_auth() or await coros_api.try_auto_login()
    if auth is None:
        # Local TTL is a guess (24h); the server often accepts the token longer.
        auth = coros_api._load_auth()
    return auth


def ymd(d):
    return d.strftime("%Y%m%d")


def last(records, field):
    for r in reversed(records):
        v = getattr(r, field)
        if v is not None:
            return v, r.date
    return None, None


def local_day(act):
    # start_time is UTC epoch seconds; bucket by local calendar day.
    try:
        return dt.datetime.fromtimestamp(int(act.start_time)).date()
    except (TypeError, ValueError):
        return dt.datetime.fromisoformat(str(act.start_time)).date()


async def main():
    auth = await get_auth()
    if auth is None:
        print("NO_AUTH: no stored COROS login. Run: ~/Repos/coros/.venv/bin/coros-mcp auth-web", file=sys.stderr)
        return 2

    with open(PLAN, encoding="utf-8") as f:
        plan = json.load(f)
    today = dt.date.today()
    plan_start = dt.date.fromisoformat(plan["meta"]["planStartDate"])

    try:
        records = await coros_api.fetch_daily_records(auth, ymd(today - dt.timedelta(days=28)), ymd(today))
        acts, page = [], 1
        while True:
            batch, total = await coros_api.fetch_activities(
                auth, ymd(min(plan_start, today - dt.timedelta(days=28))), ymd(today), page=page, size=100
            )
            acts += batch
            if len(acts) >= total or not batch:
                break
            page += 1
    except Exception as exc:  # expired/revoked token surfaces here
        print(f"NO_AUTH: COROS rejected the request ({exc}). Run: ~/Repos/coros/.venv/bin/coros-mcp auth-web", file=sys.stderr)
        return 2

    runs = {}
    for a in acts:
        if a.sport_type not in RUN_SPORTS or not a.distance_meters:
            continue
        day = local_day(a)
        r = runs.setdefault(day.isoformat(), {"km": 0.0, "hrSum": 0.0, "sec": 0})
        r["km"] += a.distance_meters / 1000
        if a.avg_hr and a.duration_seconds:
            r["hrSum"] += a.avg_hr * a.duration_seconds
            r["sec"] += a.duration_seconds

    def avg_hr(r):
        return round(r["hrSum"] / r["sec"]) if r["sec"] else None

    # Match plan workouts to what was actually run that day.
    completed, missed = {}, []
    for w in plan["weeks"]:
        for d in w["days"]:
            day = dt.date.fromisoformat(d["date"])
            if day > today:
                continue
            for x in d["workouts"]:
                if x["sport"] != "run" or x.get("type") == "race":
                    continue
                actual = runs.get(d["date"])
                planned_km = (x.get("distanceMeters") or 0) / 1000
                if actual and actual["km"] >= DONE_SHARE * planned_km:
                    completed[x["id"]] = {"km": round(actual["km"], 1), "avgHr": avg_hr(actual)}
                elif day < today and not x.get("completed"):
                    missed.append(x["id"])

    # Weekly running km since the plan started, Monday-based.
    weekly = {}
    for day, r in runs.items():
        d = dt.date.fromisoformat(day)
        if d < plan_start:
            continue
        mon = (d - dt.timedelta(days=d.weekday())).isoformat()
        weekly[mon] = round(weekly.get(mon, 0) + r["km"], 1)
    last7 = round(sum(r["km"] for day, r in runs.items() if dt.date.fromisoformat(day) > today - dt.timedelta(days=7)), 1)

    vo2, vo2_d = last(records, "vo2max")
    lthr, _ = last(records, "lthr")
    ltsp, _ = last(records, "ltsp")
    cti, _ = last(records, "cti")
    ati, _ = last(records, "ati")
    ratio, _ = last(records, "training_load_ratio")
    hrv, hrv_d = last(records, "avg_sleep_hrv")
    base, _ = last(records, "baseline")
    rhr, _ = last(records, "test_rhr")

    prev = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            prev = json.load(f)

    snap = {
        "asOf": dt.datetime.now().astimezone().isoformat(timespec="minutes"),
        "metrics": {
            "vo2max": vo2, "lthr": lthr, "ltPaceSec": ltsp, "cti": cti, "ati": ati,
            "loadRatio": ratio, "hrv": hrv, "hrvDate": hrv_d, "hrvBaseline": base, "restingHr": rhr,
            "last7Km": last7,
        },
        "weeklyKm": weekly,
        "completed": completed,
        "missed": missed,
        # Written by the daily Claude routine after this script runs; kept until replaced.
        "note": prev.get("note"),
        "noteDate": prev.get("noteDate"),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(snap, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(json.dumps({"asOf": snap["asOf"], **snap["metrics"], "completed": len(completed), "missed": len(missed)}))
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
