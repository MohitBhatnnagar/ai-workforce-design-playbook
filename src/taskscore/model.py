"""Score a task for automation suitability and recommend an autonomy level.

Two separate questions are kept apart on purpose:
  1. Is it *worth* and *feasible* to automate?  -> suitability score (0-100)
  2. How much *autonomy* is it safe to grant?   -> risk gate, which can override (1)
A task can be an excellent automation candidate and still need a human approval step.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

# Each factor is rated 1 (bad for automation) to 5 (good for automation).
# "Good" means: high volume, repeatable rules, good data, low judgement, low exception rate.
WEIGHTS = {
    "volume": 0.20,         # how often it happens
    "repeatability": 0.25,  # are the steps stable and rule-like?
    "data_quality": 0.20,   # is the input structured, complete and accessible?
    "low_judgement": 0.20,  # 5 = no judgement needed, 1 = expert judgement
    "low_exceptions": 0.15, # 5 = rarely deviates, 1 = mostly edge cases
}
assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9

ERROR_IMPACT = {"low": 1, "medium": 2, "high": 3}  # cost of one wrong output
REVERSIBLE = {"yes": 0, "no": 1}                    # can a wrong output be undone cheaply?


@dataclass(frozen=True)
class Task:
    name: str
    volume: int
    repeatability: int
    data_quality: int
    low_judgement: int
    low_exceptions: int
    error_impact: str       # low | medium | high
    reversible: str         # yes | no
    hours_per_month: float  # current human effort

    def validate(self) -> None:
        for f in WEIGHTS:
            v = getattr(self, f)
            if not isinstance(v, int) or not 1 <= v <= 5:
                raise ValueError(f"{self.name}: {f} must be an integer 1-5, got {v!r}")
        if self.error_impact not in ERROR_IMPACT:
            raise ValueError(f"{self.name}: error_impact must be one of {sorted(ERROR_IMPACT)}")
        if self.reversible not in REVERSIBLE:
            raise ValueError(f"{self.name}: reversible must be yes or no")
        if self.hours_per_month < 0:
            raise ValueError(f"{self.name}: hours_per_month cannot be negative")


@dataclass(frozen=True)
class Assessment:
    task: Task
    suitability: float      # 0-100
    risk: int               # 1-4
    autonomy: str           # auto | approve | human
    priority: float         # suitability weighted by hours at stake
    rationale: str


def suitability(t: Task) -> float:
    raw = sum(getattr(t, f) * w for f, w in WEIGHTS.items())  # 1..5
    return round((raw - 1) / 4 * 100, 1)


def risk_level(t: Task) -> int:
    """1 (benign) to 4 (high impact AND irreversible)."""
    return ERROR_IMPACT[t.error_impact] + REVERSIBLE[t.reversible]


def autonomy(score: float, risk: int) -> tuple[str, str]:
    if risk >= 4:
        return "human", "high-impact and irreversible: agent may prepare, a person decides"
    if score < 40:
        return "human", "poor automation fit: keep with people, revisit after fixing inputs"
    if risk == 3 or score < 70:
        return "approve", "automate the work, keep a human approval step"
    return "auto", "good fit and contained risk: run unattended with sampling and audit"


def assess(t: Task) -> Assessment:
    t.validate()
    s, r = suitability(t), risk_level(t)
    mode, why = autonomy(s, r)
    return Assessment(t, s, r, mode, round(s * t.hours_per_month / 100, 1), why)


def rank(tasks: list[Task]) -> list[Assessment]:
    """Highest priority first: suitable work with many hours at stake. Ties broken by name."""
    return sorted((assess(t) for t in tasks), key=lambda a: (-a.priority, a.task.name))


def load_csv(path: str | Path) -> list[Task]:
    with open(path, newline="", encoding="utf-8") as f:
        return [Task(r["name"], int(r["volume"]), int(r["repeatability"]), int(r["data_quality"]),
                     int(r["low_judgement"]), int(r["low_exceptions"]), r["error_impact"],
                     r["reversible"], float(r["hours_per_month"])) for r in csv.DictReader(f)]


def report(assessments: list[Assessment]) -> str:
    head = f"{'task':<28}{'fit':>6}{'risk':>6}  {'autonomy':<9}{'priority':>9}"
    rows = [f"{a.task.name:<28}{a.suitability:>6.1f}{a.risk:>6}  {a.autonomy:<9}{a.priority:>9.1f}" for a in assessments]
    return "\n".join([head, *rows])
