import os
import unittest

from taskscore import Task, assess, autonomy, load_csv, rank, report, risk_level, suitability
from taskscore.cli import main

CSV = os.path.join(os.path.dirname(__file__), "..", "examples", "tasks.csv")


def t(**kw):
    base = dict(name="x", volume=3, repeatability=3, data_quality=3, low_judgement=3, low_exceptions=3,
                error_impact="low", reversible="yes", hours_per_month=100)
    base.update(kw)
    return Task(**base)


class ScoreTests(unittest.TestCase):
    def test_bounds(self):
        self.assertEqual(suitability(t(volume=1, repeatability=1, data_quality=1, low_judgement=1, low_exceptions=1)), 0.0)
        self.assertEqual(suitability(t(volume=5, repeatability=5, data_quality=5, low_judgement=5, low_exceptions=5)), 100.0)

    def test_midpoint(self):
        self.assertEqual(suitability(t()), 50.0)

    def test_repeatability_matters_more_than_volume(self):
        a = suitability(t(repeatability=5, volume=1))
        b = suitability(t(repeatability=1, volume=5))
        self.assertGreater(a, b)

    def test_risk_levels(self):
        self.assertEqual(risk_level(t(error_impact="low", reversible="yes")), 1)
        self.assertEqual(risk_level(t(error_impact="high", reversible="no")), 4)
        self.assertEqual(risk_level(t(error_impact="medium", reversible="no")), 3)


class AutonomyTests(unittest.TestCase):
    def test_high_fit_low_risk_is_auto(self):
        self.assertEqual(autonomy(85, 1)[0], "auto")

    def test_risk_overrides_fit(self):
        self.assertEqual(autonomy(95, 4)[0], "human")

    def test_poor_fit_stays_human(self):
        self.assertEqual(autonomy(20, 1)[0], "human")

    def test_middling_fit_needs_approval(self):
        self.assertEqual(autonomy(55, 1)[0], "approve")

    def test_risk_three_needs_approval_even_if_great_fit(self):
        self.assertEqual(autonomy(90, 3)[0], "approve")


class ValidationTests(unittest.TestCase):
    def test_rating_out_of_range(self):
        with self.assertRaises(ValueError):
            assess(t(volume=6))

    def test_non_integer_rating(self):
        with self.assertRaises(ValueError):
            assess(t(volume=3.5))

    def test_bad_enums(self):
        with self.assertRaises(ValueError):
            assess(t(error_impact="catastrophic"))
        with self.assertRaises(ValueError):
            assess(t(reversible="maybe"))

    def test_negative_hours(self):
        with self.assertRaises(ValueError):
            assess(t(hours_per_month=-1))


class RankingTests(unittest.TestCase):
    def setUp(self):
        self.ranked = rank(load_csv(CSV))
        self.by = {a.task.name: a for a in self.ranked}

    def test_loads_all_rows(self):
        self.assertEqual(len(self.ranked), 10)

    def test_formatting_qa_is_a_prime_candidate(self):
        a = self.by["Format and template QA"]
        self.assertEqual(a.autonomy, "auto")
        self.assertGreater(a.suitability, 85)

    def test_high_impact_irreversible_never_auto(self):
        for name in ("Refund and credit decisions", "Contract and legal review"):
            self.assertEqual(self.by[name].autonomy, "human")

    def test_client_reply_drafting_keeps_a_human_in_the_loop(self):
        self.assertEqual(self.by["Client reply drafting"].autonomy, "approve")

    def test_creative_direction_stays_with_people(self):
        self.assertEqual(self.by["Creative direction"].autonomy, "human")

    def test_priority_is_sorted_descending(self):
        p = [a.priority for a in self.ranked]
        self.assertEqual(p, sorted(p, reverse=True))

    def test_report_renders_every_task(self):
        out = report(self.ranked)
        for a in self.ranked:
            self.assertIn(a.task.name, out)

    def test_cli_returns_2_on_missing_file(self):
        self.assertEqual(main([os.path.join(os.path.dirname(CSV), "missing.csv")]), 2)

    def test_cli_returns_0_on_good_file(self):
        self.assertEqual(main([CSV]), 0)


if __name__ == "__main__":
    unittest.main()
