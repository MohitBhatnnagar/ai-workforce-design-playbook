# The method

## 1. Inventory

Ask the people who do the work, not their managers. For each task capture: name, how often it happens, hours per month across the team, the input it needs, the output it produces, what happens when it goes wrong, and whether a wrong output can be undone.

Rules of thumb:

- Task level, not role level. "Check a brief for completeness" is a task; "operations" is not.
- Include the invisible work: chasing, reformatting, copying between systems. It is often the best automation target.
- Record the exception paths. Most of the cost of a process lives in its exceptions.

## 2. Score fit

Rate each factor 1 to 5 (5 is good for automation). Use the anchors below so ratings are comparable between assessors.

| Factor | 1 | 3 | 5 |
|---|---|---|---|
| Volume | a few a month | weekly | many per day |
| Repeatability | different every time | mostly the same, some variation | same steps every time |
| Data quality | scattered, missing, informal | usable with cleanup | structured, complete, accessible |
| Low judgement | expert judgement | experienced judgement | a rule or checklist decides |
| Low exceptions | mostly edge cases | 1 in 4 is unusual | rarely deviates |

Run `taskscore` for the weighted score. Have two or three people score independently and discuss differences of two points or more.

## 3. Gate on risk

Ask two questions of every task, independently of fit:

1. **How costly is one wrong output?** Low (annoying), medium (client-visible or rework), high (money, legal, safety, reputation).
2. **Can it be undone cheaply?** An email to a client cannot; a draft in a queue can.

High impact plus irreversible means a person decides, whatever the fit. This is the rule that keeps an excellent automation candidate from doing something expensive unattended.

## 4. Design the hand-offs

See [handoffs.md](handoffs.md). This is the step teams skip, and where automation programmes fail: the agent works, but nobody owns its exceptions.

## 5. Run and measure

| Metric | Why |
|---|---|
| First-pass yield of automated output | Is it as good as the human baseline? |
| Exception rate, and time to resolve | Is the escalation path working? |
| Human override rate | A high rate means the agent is wrong or the policy is too loose |
| Hours returned, and where they went | The benefit only counts if the time is reused |
| Cost per task including model and review | Unit economics, not just licence cost |

Pilot protocol: run the agent in **shadow mode** (it produces output, a human still does the work), compare, then move to `approve`, then to `auto` only for tasks whose yield and override rate hold for several weeks.

## Common failure modes

- Automating the process as it is instead of fixing it first. Automation makes a bad process faster.
- No owner for exceptions, so they pile up silently.
- Measuring hours saved but not quality.
- Moving to `auto` after a good demo instead of a good month.
