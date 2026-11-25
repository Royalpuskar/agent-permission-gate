import unittest
from guard import Guard, PermissionDenied

class GuardTests(unittest.TestCase):
    def setUp(self):
        self.calls = []
        self.grants = [dict(subject="agent", action="send", resource="report",
                            expires=200, effect="allow", approval_required=True)]
        self.guard = Guard("agent", self.grants, clock=lambda: 100)

    def tool(self):
        self.calls.append("executed")
        return 42

    def test_denied_action_never_runs(self):
        with self.assertRaises(PermissionDenied):
            self.guard.run("send", "report", self.tool)
        self.assertEqual(self.calls, [])

    def test_approved_action_runs(self):
        self.assertEqual(self.guard.run("send", "report", self.tool, approved=True), 42)
        self.assertEqual(self.calls, ["executed"])

    def test_nonboolean_approval_denied(self):
        with self.assertRaises(PermissionDenied):
            self.guard.run("send", "report", self.tool, approved="false")
        self.assertEqual(self.calls, [])

    def test_unknown_resource_denied(self):
        self.assertFalse(self.guard.check("send", "other", approved=True)["allowed"])

    def test_policy_snapshot(self):
        self.grants.clear()
        self.assertTrue(self.guard.check("send", "report", approved=True)["allowed"])

    def test_invalid_policy_denied(self):
        guard = Guard("agent", [{}], clock=lambda: 100)
        self.assertFalse(guard.check("send", "report")["allowed"])

if __name__ == "__main__":
    unittest.main()
