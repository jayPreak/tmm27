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

## Using the skill

Symlink it into Claude Code's skills folder. It needs the `coros` MCP server ([coros-mcp](https://github.com/cygnusb/coros-mcp) or a fork) connected and authenticated.

```bash
ln -s "$PWD/skill/coros-coach" ~/.claude/skills/coros-coach
```

The methodology reference docs are adapted from [claude-coach](https://www.npmjs.com/package/claude-coach) (MIT).
