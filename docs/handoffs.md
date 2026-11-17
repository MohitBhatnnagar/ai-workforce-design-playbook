# Designing hand-offs between agents and people

An agent that works is not enough. Four things must be decided for every automated task before it goes live.

## 1. Decision rights

For each task, write down in one line each: who can **start** it, who **approves** it (if anyone), who **owns the result**, who can **stop** it. A short RACI table is enough:

| Task | Agent | Reviewer | Process owner | Escalation owner |
|---|---|---|---|---|
| Request intake and routing | R | sampled A | Ops lead | Team lead |
| Client reply drafting | R (draft) | A (approve) | Account lead | Ops lead |
| Refund decision | prepares case | R, A | Finance owner | Director |

## 2. The exception path

Every automated task has three exits: **done**, **needs approval**, **cannot handle**. The third is the one that must be designed.

- Define what counts as an exception in observable terms: low confidence, missing field, rule violation, repeated failure, unusual value.
- Route it to a *named queue with an owner and a time limit*, not to a shared inbox.
- Give the owner the context: the input, what the agent tried, why it stopped.
- Log every exception with a cause category, and review the top causes weekly. Recurring exceptions are process defects to fix, or candidates to automate next.

## 3. Quality checks on the automation itself

- **Sampling.** Review a fixed percentage of unattended output, higher at launch and lower once yield is stable.
- **Calibration.** Reviewers sample the same items so their standard matches, and an AI reviewer is calibrated against them.
- **Drift watch.** A control chart on first-pass yield and override rate, with alerts on run-rule signals, catches a model or input change before a client does.
- **Kill switch.** One named person can pause an automation without a deployment.

## 4. Capability and cost

- Which skills move from doing the task to reviewing it, and how do you train for that?
- What is the cost per task including model usage, review time and exception handling? Compare with the human baseline, not with zero.
- Which saved hours are reinvested, and where? Savings that vanish into slack are not savings.

## The one-page checklist

Before a task goes to `approve` or `auto`:

- [ ] Decision rights written down and agreed
- [ ] Exception definition, queue, owner and time limit
- [ ] Sampling rate and quality metric chosen
- [ ] Kill switch owner named
- [ ] Shadow-mode comparison against the human baseline completed
- [ ] Cost per task calculated
- [ ] Audit trail captures input, output, decision and who approved
