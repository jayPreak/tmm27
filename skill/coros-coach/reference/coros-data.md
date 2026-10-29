# COROS data → coaching signals

## `get_daily_metrics` fields

| Field | Meaning | Use |
|---|---|---|
| `avg_sleep_hrv` | Nightly HRV (RMSSD, ms) | Readiness — compare to `baseline` and own 7-day mean |
| `baseline` | COROS rolling HRV baseline | Reference for HRV % change |
| `test_rhr` | Measured resting HR (what the app shows) | Readiness; use this, not `rhr` |
| `rhr` | Daily aggregate HR (web dashboard) | Ignore for readiness |
| `training_load` | That day's load (≈ TSS-like) | Weekly load totals |
| `ati` / `cti` | Acute (≈7d) / chronic (≈42d) training index | Fatigue / fitness (≈ ATL / CTL) |
| `training_load_ratio` | ATI / CTI | Ramp risk: <0.8 detraining, 0.8–1.5 productive, >1.5 risky |
| `tired_rate` | COROS fatigue | Form (≈ TSB, negative = fatigued) |
| `vo2max` | VO2max estimate (last ~28 d only) | Trend; race prediction sanity check |
| `lthr` | Lactate threshold HR (bpm) | Anchor run HR zones |
| `ltsp` | Lactate threshold pace (s/km) | Anchor run pace zones (convert to min/km) |
| `stamina_level`, `stamina_level_7d` | Base fitness and its 7-day trend | Is the base growing? |

Dates are `YYYYMMDD`. Distance in m, duration in s. Activity `calories` are in cal — divide by 1000 for kcal.

## Zone anchors from COROS

- **Run HR** (from `lthr`, Friel-style): Z1 <85%, Z2 85–89%, Z3 90–94%, Z4 95–99%, Z5a 100–102%, Z5b+ >102% of LTHR.
- **Run pace** (from `ltsp` = threshold pace T): easy ≈ T+60–90 s/km, marathon ≈ T+15–25 s/km, threshold ≈ T ±5 s/km, VO2 intervals ≈ T−15–20 s/km.
- **Bike**: COROS gives no FTP — ask, or estimate from a recent 20-min best power ×0.95 in `get_activity_detail`. Zones in `reference/zones.md`.
- **Swim**: ask for CSS (or a 400m/200m test). COROS gives no swim threshold.

Always say the zones are derived from COROS estimates and offer a field test if they look off (e.g. LTHR way out of line with recent race efforts).

## Daily readiness rules

Compute from the last ~10 days of `get_daily_metrics` + last night's sleep:

| Signal | Green | Yellow | Red |
|---|---|---|---|
| HRV vs 7-day mean (or `baseline`) | within −5% | −5 to −15% | worse than −15%, or 3+ days trending down |
| `test_rhr` vs 7-day mean | ≤ +2 bpm | +3–5 bpm | > +5 bpm |
| Sleep (if available) | ≥ 7 h | 6–7 h | < 6 h |
| `training_load_ratio` | 0.8–1.3 | 1.3–1.5 | > 1.5 |
| Athlete's own feel / soreness | good | meh | bad, pain, illness |

- All green → do the planned session.
- Any yellow → keep the session but cut intensity one zone or volume ~20%; move a key session if two yellows.
- Any red → easy Z1 only or rest. Pain or illness symptoms always override the numbers.

One bad night alone is noise; act on trends (2–3 days) unless the athlete feels bad.

## Weekly review checklist

1. Planned vs done per session (`list_planned_activities` vs `list_activities`): match on date + sport.
2. Volume per sport vs target; intensity split (time in Z1–2 vs Z3+ from `get_activity_detail` HR zones for key sessions).
3. Easy-run decoupling: HR creeping up at the same easy pace across weeks = fatigue or heat.
4. HRV / RHR trend across the week, `training_load_ratio` at week end.
5. Unplanned sessions, skipped long sessions, volume spikes.
