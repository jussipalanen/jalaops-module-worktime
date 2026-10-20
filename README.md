# Työaikalaskuri (JalaOps module)

A [JalaOps](https://github.com/jussipalanen/jalaops) Python module as a Composer package: hours worked and labour cost from a shift's start and end times. A shift that ends before it starts goes past midnight.

Version 2 is a class that uses the JalaOps module SDK (`class WorktimeModule(Module)`), so it needs JalaOps 1.15.0 or later. Version 1 works with older JalaOps versions.

Install it in the JalaOps backend:

```bash
./dev modules:add https://github.com/jussipalanen/jalaops-module-worktime.git
# or with Composer:
./dev composer config repositories.worktime vcs https://github.com/jussipalanen/jalaops-module-worktime.git
./dev composer require jalaops/worktime:^2.0
```

Try it on its own, with the SDK from a JalaOps checkout next to this one on the path:

```bash
export PYTHONPATH=../jalaops/backend/modules/sdk
echo '{"start": "07:30", "end": "16:00", "break_minutes": 30, "hourly_rate": 45}' | python3 main.py
python3 -m unittest                                       # tests
```

Release a new version by tagging it (`git tag -a v1.1.0`); JalaOps picks it up with `composer update jalaops/worktime`.
