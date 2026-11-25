import json
import unittest
from pathlib import Path
from guard import Guard
from preflight import preflight

class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path(__file__).with_name("workflow_demo.json").read_text())
        self.guard = Guard(self.data["subject"], self.data["grants"], clock=lambda: 100)

    def test_demo(self):
        result = preflight(self.data["plan"], self.guard, self.data["budget"])
        self.assertFalse(result["ready"])
        self.assertEqual(result["estimated_allowed_cost"], "0.50")
        self.assertEqual([r["reason"] for r in result["steps"]],
                         ["active-grant", "approval-required", "dependency-blocked", "budget-exceeded"])

    def test_forward_dependency_rejected(self):
        step = dict(self.data["plan"][0], depends_on=["missing"])
        with self.assertRaises(ValueError):
            preflight([step], self.guard, 2)

    def test_negative_budget_rejected(self):
        with self.assertRaises(ValueError):
            preflight([], self.guard, -1)

    def test_duplicate_id_rejected(self):
        step = self.data["plan"][0]
        with self.assertRaises(ValueError):
            preflight([step, step], self.guard, 2)
