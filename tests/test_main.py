"""Tests for the work time module. Run them with the JalaOps module SDK on the
path: PYTHONPATH=../jalaops/backend/modules/sdk python3 -m unittest
"""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from jalaops_module import InputError

from main import WorktimeModule

ROOT = Path(__file__).resolve().parent.parent


class WorktimeTest(unittest.TestCase):
    def setUp(self):
        self.module = WorktimeModule()

    def calculate(self, **values):
        return self.module.handle({"start": "07:30", "end": "16:00", **values})

    def test_hours_and_cost(self):
        self.assertEqual(
            self.calculate(break_minutes=30, hourly_rate=45),
            {"duration": "8 h 0 min", "hours": 8.0, "overtime": 0.0, "cost": 360.0},
        )

    def test_overtime_past_8_hours(self):
        self.assertEqual(self.calculate(end="18:15")["overtime"], 2.75)

    def test_a_shift_past_midnight(self):
        self.assertEqual(self.calculate(start="22:00", end="06.30", break_minutes=30)["duration"], "8 h 0 min")

    def test_no_cost_without_an_hourly_rate(self):
        self.assertNotIn("cost", self.calculate())
        self.assertNotIn("cost", self.calculate(hourly_rate=None))

    def test_it_checks_the_input(self):
        for values, message in [
            ({"start": "7"}, "Alkoi: anna aika muodossa hh:mm."),
            ({"end": "24:00"}, "Päättyi: anna aika muodossa hh:mm."),
            ({"start": 730}, "Alkoi: anna tekstiä."),
            ({"break_minutes": -5}, "Tauot: anna nolla tai positiivinen luku."),
            ({"break_minutes": "30"}, "Tauot: anna numero."),
            ({"hourly_rate": -1}, "Tuntihinta: anna nolla tai positiivinen luku."),
            ({"break_minutes": 600}, "Tauot ovat pidemmät kuin työaika."),
        ]:
            with self.subTest(values=values), self.assertRaises(InputError) as raised:
                self.calculate(**values)
            self.assertEqual(str(raised.exception), message)

        with self.assertRaisesRegex(InputError, "^Päättyi: pakollinen tieto.$"):
            self.module.handle({"start": "07:30"})

    def test_it_runs_like_jalaops_runs_it(self):
        """JSON in on stdin and out on stdout, with only these variables."""
        result = subprocess.run(
            [sys.executable, "-s", "-B", "-X", "utf8", "main.py"],
            input=json.dumps({"start": "08:00", "end": "12:00"}),
            capture_output=True,
            text=True,
            cwd=ROOT,
            env={"PATH": os.environ.get("PATH", ""), "LANG": "C.UTF-8", "PYTHONPATH": os.environ.get("PYTHONPATH", "")},
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"duration": "4 h 0 min", "hours": 4.0, "overtime": 0.0})


if __name__ == "__main__":
    unittest.main()
