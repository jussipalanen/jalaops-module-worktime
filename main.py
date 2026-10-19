"""Work time module for JalaOps: hours worked and labour cost.

Input:  {"start": "07:30", "end": "16:00", "break_minutes": 30, "hourly_rate": 45}
Output: {"duration": "8 h 0 min", "hours": 8.0, "overtime": 0.0, "cost": 360.0}

Hours past 8 are overtime.

A shift that ends before it starts goes past midnight.
"""

import json
import re
import sys


def fail(message):
    """Ends with an error; the app shows the message to the user."""
    print(message, file=sys.stderr)
    sys.exit(1)


def minutes(value, label):
    """Minutes since midnight from a "hh:mm" (or "hh.mm") time."""
    match = re.fullmatch(r"(\d{1,2})[:.](\d{2})", str(value).strip())
    if not match or int(match[1]) > 23 or int(match[2]) > 59:
        fail(f"{label}: anna aika muodossa hh:mm.")
    return int(match[1]) * 60 + int(match[2])


def number(value, label):
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
        fail(f"{label}: anna nolla tai positiivinen luku.")
    return value


data = json.load(sys.stdin)

start = minutes(data.get("start"), "Alkoi")
end = minutes(data.get("end"), "Päättyi")
pause = number(data.get("break_minutes", 0), "Tauot")

worked = (end - start) % (24 * 60) - pause
if worked <= 0:
    fail("Tauot ovat pidemmät kuin työaika.")

output = {
    "duration": f"{int(worked // 60)} h {int(worked % 60)} min",
    "hours": round(worked / 60, 2),
    "overtime": round(max(0, worked - 8 * 60) / 60, 2),
}

if "hourly_rate" in data:
    output["cost"] = round(worked / 60 * number(data["hourly_rate"], "Tuntihinta"), 2)

json.dump(output, sys.stdout, ensure_ascii=False)
