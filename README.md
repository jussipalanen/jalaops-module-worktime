# Työaikalaskuri (JalaOps module)

A [JalaOps](https://github.com/jussipalanen/jalaops) Python module as a Composer package: hours worked and labour cost from a shift's start and end times. A shift that ends before it starts goes past midnight.

Install it in the JalaOps backend:

```bash
./dev composer config repositories.worktime vcs https://github.com/jussipalanen/jalaops-module-worktime.git
./dev composer require jalaops/worktime:^1.0
```

Try it on its own: `echo '{"start": "07:30", "end": "16:00", "break_minutes": 30, "hourly_rate": 45}' | python3 main.py`

Release a new version by tagging it (`git tag -a v1.1.0`); JalaOps picks it up with `composer update jalaops/worktime`.
