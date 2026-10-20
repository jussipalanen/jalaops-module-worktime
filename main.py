"""Work time module for JalaOps: hours worked and labour cost.

Input:  {"start": "07:30", "end": "16:00", "break_minutes": 30, "hourly_rate": 45}
Output: {"duration": "8 h 0 min", "hours": 8.0, "overtime": 0.0, "cost": 360.0}

Hours past 8 are overtime.

A shift that ends before it starts goes past midnight.

It uses the JalaOps module SDK (jalaops_module, JalaOps 1.15.0 or later),
which JalaOps puts on the module's PYTHONPATH.
"""

import re

from jalaops_module import InputError, Module, action

# The names users see in the error messages.
LABELS = {"start": "Alkoi", "end": "Päättyi", "break_minutes": "Tauot", "hourly_rate": "Tuntihinta"}


def minutes(value, label):
    """Minutes since midnight from a "hh:mm" (or "hh.mm") time."""
    match = re.fullmatch(r"(\d{1,2})[:.](\d{2})", value.strip())
    if not match or int(match[1]) > 23 or int(match[2]) > 59:
        raise InputError(f"{label}: anna aika muodossa hh:mm.")
    return int(match[1]) * 60 + int(match[2])


def not_negative(value, label):
    if value < 0:
        raise InputError(f"{label}: anna nolla tai positiivinen luku.")
    return value


class WorktimeModule(Module):
    @action("calculate", default=True, labels=LABELS)
    def calculate(self, start: str, end: str, break_minutes: float = 0, hourly_rate: float | None = None):
        worked = (minutes(end, "Päättyi") - minutes(start, "Alkoi")) % (24 * 60) - not_negative(break_minutes, "Tauot")
        if worked <= 0:
            raise InputError("Tauot ovat pidemmät kuin työaika.")

        output = {
            "duration": f"{int(worked // 60)} h {int(worked % 60)} min",
            "hours": round(worked / 60, 2),
            "overtime": round(max(0, worked - 8 * 60) / 60, 2),
        }

        if hourly_rate is not None:
            output["cost"] = round(worked / 60 * not_negative(hourly_rate, "Tuntihinta"), 2)

        return output


if __name__ == "__main__":
    WorktimeModule.main()
