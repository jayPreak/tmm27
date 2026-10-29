# TMM27

Training plans for the Tata Mumbai Marathon (17 January 2027), and the `coros-coach` Claude Code skill that builds them.

Live site: https://tmm-2027-plan.vercel.app

| Plan | Link | Built from |
|---|---|---|
| Jayesh 3:45 | `/#jayesh` | Jayesh's COROS watch data (VO2max, threshold HR/pace, HRV, load) |
| Open 3:20 | `/#open-320` | General plan for any runner, no personal data |

Both plans run four days a week: Tuesday (quality), Wednesday (easy), Friday (marathon pace), Sunday (long run).

## Layout

```
skill/coros-coach/   Claude Code skill: coaching rules + COROS MCP workflow
plans/               Plan data (JSON, claude-coach schema) + rendered HTML
scripts/             Plan generators and the site build
src/                 Site source (styles.css, body.html with the page script)
web/index.html       Built site, served by Vercel
```

## Update a plan

```bash
python3 scripts/gen_jayesh_345.py   # or gen_open_320.py
python3 scripts/build_site.py
git commit -am "Update plan" && git push
```

Every push to `main` deploys to Vercel.

## Daily COROS update

A Claude Code scheduled task (`tmm27-daily-coros-update`, 11:00 local, on Jayesh's Mac) runs each day:

1. `~/Repos/coros/.venv/bin/python scripts/update_from_coros.py` reads COROS (read-only) into `plans/jayesh-snapshot.json`: VO2max, threshold HR and pace, CTI, HRV vs baseline, last 7 days km, and which planned runs were done or missed.
2. Claude writes a short "Today's call" note into the snapshot using the skill's readiness rules.
3. `scripts/build_site.py` rebuilds `web/index.html`, and the change is committed and pushed, which redeploys the site.

If the COROS login has expired, the run stops and asks for `coros-mcp auth-web`. The routine never edits the COROS calendar or the plan's workouts.

## Using the skill

Symlink it into Claude Code's skills folder. It needs the `coros` MCP server ([coros-mcp](https://github.com/cygnusb/coros-mcp) or a fork) connected and authenticated.

```bash
ln -s "$PWD/skill/coros-coach" ~/.claude/skills/coros-coach
```

The methodology reference docs are adapted from [claude-coach](https://www.npmjs.com/package/claude-coach) (MIT).
