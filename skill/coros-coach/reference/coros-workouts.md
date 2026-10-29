# Pushing workouts to the COROS calendar

Workouts scheduled here appear in the COROS app's training calendar and sync to the watch. Always show the athlete the list (date, name, steps) and get a yes before scheduling.

## What COROS MCP can schedule

| Sport | Tool | `sport_type` | Default target |
|---|---|---|---|
| Run (road / trail / track / treadmill) | `schedule_workout` | `100` (`102` trail, `103` track) | HR (`intensity_type` 2, bpm) |
| Indoor bike | `schedule_workout` | `2` | Power (`intensity_type` 6, watts) |
| Road bike | `schedule_workout` | `200` | Power (watts) |
| Strength | `schedule_strength_workout` | — | reps (`target_type` 3) or seconds (`target_type` 2) |
| **Swim** | **not supported** | — | Give swim sessions as text in the plan (and in `plan.html`); tell the athlete to enter them manually in the COROS app if they want them on the watch |

Never pass `sport_type: 1` (wire ID — rejected). For pace targets on runs use `intensity_type: 3` with intensity values in **seconds per km** (e.g. 4:30/km → 270). Keep `intensity_low` < `intensity_high` numerically, so `intensity_low` is the faster pace.

## Step shapes

Exactly one duration key per step: `duration_minutes`, `duration_meters`, or `duration_open: true` (lap button).

```json
{
  "name": "Run – 6x800m VO2",
  "happen_day": "20261104",
  "sport_type": 100,
  "intensity_type": 3,
  "steps": [
    {"name": "Warm-up", "duration_minutes": 15, "intensity_low": 330, "intensity_high": 360},
    {"repeat": 6, "steps": [
      {"name": "800m hard", "duration_meters": 800, "intensity_low": 225, "intensity_high": 235},
      {"name": "Jog", "duration_minutes": 2, "intensity_low": 360, "intensity_high": 420}
    ]},
    {"name": "Cool-down", "duration_minutes": 10, "intensity_low": 340, "intensity_high": 400}
  ]
}
```

HR-based easy run (default intensity type for runs):

```json
{"name": "Easy Z2 45min", "happen_day": "20261105", "sport_type": 100,
 "steps": [{"name": "Z2", "duration_minutes": 45, "intensity_low": 135, "intensity_high": 148}]}
```

Bike sweet spot (watts, FTP 250):

```json
{"name": "Bike – 3x12 Sweet Spot", "happen_day": "20261106", "sport_type": 2,
 "steps": [
  {"name": "Warm-up", "duration_minutes": 10, "intensity_low": 125, "intensity_high": 175},
  {"repeat": 3, "steps": [
    {"name": "Sweet spot", "duration_minutes": 12, "intensity_low": 220, "intensity_high": 235},
    {"name": "Easy", "duration_minutes": 4, "intensity_low": 120, "intensity_high": 150}]},
  {"name": "Cool-down", "duration_minutes": 10, "intensity_low": 110, "intensity_high": 150}]}
```

Strength: resolve exercises first with `list_exercises(sport_type=4)` — each exercise needs `origin_id`, `name` (T-code) and `overview` (sid_… key) from the catalogue. Omit weight for bodyweight.

## Multiple sessions per day

Use `sort_no` (1, 2, …) for order within the day (e.g. brick: bike `sort_no` 1, run `sort_no` 2).

## Changing the calendar

- See what's there: `list_planned_activities(start_day, end_day)`.
- Remove: `remove_scheduled_workout(plan_id, id_in_plan, plan_program_id)` — IDs come from the `schedule_workout` response (when `enrichment_ok` is true) or from `list_planned_activities`.
- Move/replace: remove then schedule again. Only touch entries you created or the athlete named.
- After scheduling a batch, re-list the range and report what's on the calendar now.
