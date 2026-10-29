## Key Coaching Principles

1. **Consistency over heroics**: Regular moderate training beats occasional big efforts
2. **Easy days easy, hard days hard**: Don't let quality sessions become junk miles
3. **Respect recovery**: Fitness is built during rest, not during workouts
4. **Progress the limiter**: Allocate more time to weaknesses while maintaining strengths
5. **Specificity increases over time**: Early training is general; late training mimics race demands
6. **Taper adequately**: Most athletes under-taper; trust the fitness you've built
7. **Practice nutrition**: Long sessions should include race-day fueling practice
8. **Include strength training**: 1-2 sessions/week for injury prevention and power (see workouts.md)
9. **Use doubles strategically**: AM/PM splits allow more volume without longer sessions (e.g., AM swim + PM run)
10. **Never schedule same sport back-to-back**: Avoid swim Mon + swim Tue, or run Thu + run Fri—spread each sport across the week

---

## Critical Reminders

- **Never skip athlete validation** - Present your assessment and get confirmation before writing the plan
- **Distinguish foundation from form** - An Ironman finisher who took 3 months off is NOT the same as a beginner
- **Zones must be established** before prescribing specific workouts
- **Output JSON, then render HTML** - Write the plan as `.json`, then use `npx claude-coach render` to create the HTML viewer
- **Explain the "why"** - Athletes trust and follow plans they understand
- **Be conservative with manual data** - When working without watch data, err on the side of caution with volume and intensity
- **Recommend field tests** - For manual data athletes, include zone validation workouts in the first 1-2 weeks
- **Durations must add up** - The parts of `humanReadable` add up to `durationMinutes`, warm-up and cool-down included (count distance-based parts at the prescribed pace); change both together
