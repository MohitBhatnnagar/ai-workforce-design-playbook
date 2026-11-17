# AI Workforce Design Playbook

A method for deciding **which work AI agents should do alone, which needs a human approval step, and which should stay with people**, plus a small scoring tool that makes the decision repeatable.

Most automation programmes start with a tool ("we have n8n, what can we automate?") and end with a pile of brittle workflows. This playbook starts with the work: take an inventory of tasks, score them on a small set of factors, separate *fit* from *risk*, and design the hand-offs between agents and people before building anything.

## The method in five steps

| Step | Output | Doc |
|---|---|---|
| 1. Inventory the work | A task list with monthly effort, from the people doing it | [docs/method.md](docs/method.md#1-inventory) |
| 2. Score fit | Suitability 0 to 100 per task | [docs/method.md](docs/method.md#2-score-fit) |
| 3. Gate on risk | Autonomy level: **auto / approve / human** | [docs/method.md](docs/method.md#3-gate-on-risk) |
| 4. Design the hand-offs | Who reviews, how exceptions reach an owner, how quality is checked | [docs/handoffs.md](docs/handoffs.md) |
| 5. Run and measure | Yield, exception rate, hours returned, cost per task | [docs/method.md](docs/method.md#5-run-and-measure) |

## The tool

```bash
pip install -e .
taskscore examples/tasks.csv
```

```
task                           fit  risk  autonomy  priority
Format and template QA        91.3     1  auto          136.9
Request intake and routing    86.2     1  auto          103.4
First-pass content review     50.0     2  approve      100.0
Client reply drafting         46.2     3  approve       50.8
Creative direction            18.8     2  human         15.0
Refund and credit decisions   41.2     4  human         10.3
Contract and legal review     25.0     4  human          7.5
```

The inventory in `examples/tasks.csv` is **synthetic**. Replace it with your own.

Two ideas the output shows:

- **Fit and risk are separate.** "Client reply drafting" is a decent automation candidate (fit 46) but an irreversible, medium-impact output, so it gets `approve`, not `auto`. "Refund and credit decisions" scores only 41 on fit *and* is high-impact and irreversible, so it stays `human` and the agent may only prepare the case.
- **Priority is fit times hours at stake.** A moderately suitable task with 200 hours a month ("First-pass content review") can beat a perfectly suitable task with 40 hours.

## How the score is built

Five factors, each rated 1 to 5 where 5 is good for automation: volume, repeatability, data quality, absence of judgement, absence of exceptions. Weights are explicit in `model.py` (repeatability 25%, the rest 15 to 20%) and are meant to be argued about and changed. Risk is separate: error impact (low, medium, high) plus reversibility (can a wrong output be cheaply undone?).

| Autonomy | Rule | Meaning |
|---|---|---|
| `human` | risk 4, or fit below 40 | A person decides. An agent may prepare. |
| `approve` | risk 3, or fit below 70 | The agent does the work, a person approves before it takes effect |
| `auto` | fit 70 or more and risk 1 or 2 | Runs unattended, with sampling and audit |

These map directly onto the policy in [`agentflow-hitl`](https://github.com/MohitBhatnnagar/agentflow-hitl) (`AUTO`, `APPROVE`, `ESCALATE`), which enforces them at run time.

## Tests

22 tests cover score bounds, weight sensitivity, the risk-overrides-fit rule, input validation and ranking of the example inventory.

```bash
python -m unittest discover -s tests -v
```

## Limits

- Ratings are judgements. Two assessors will differ, so calibrate by having several people score the same ten tasks and discussing the gaps, just as reviewers are calibrated in [`ai-quality-and-evals`](https://github.com/MohitBhatnnagar/ai-quality-and-evals).
- The score ranks candidates; it does not replace a pilot. Always measure a pilot against the human baseline before scaling.
- Hours at stake come from self-reported effort. Sample real work for a week to check.

## License

MIT
