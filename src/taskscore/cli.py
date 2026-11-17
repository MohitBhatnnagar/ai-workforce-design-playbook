from __future__ import annotations

import argparse
import sys

from .model import load_csv, rank, report


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="taskscore", description="Rank tasks for automation and autonomy level")
    p.add_argument("csv", help="task inventory CSV (see examples/tasks.csv)")
    a = p.parse_args(argv)
    try:
        print(report(rank(load_csv(a.csv))))
    except (ValueError, KeyError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
