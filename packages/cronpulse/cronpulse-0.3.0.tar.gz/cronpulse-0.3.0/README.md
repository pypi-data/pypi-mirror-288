# Cronpulse

Cronpulse is a simple Python package to monitor and wrap cron jobs with state pings.

## Installation

```bash
pip install cronpulse
```

## Using Monitor directly

```python
monitor = Monitor("your_job_key")
monitor.ping("run")
# Your job logic here
monitor.ping("complete")
```

## Using wrap function

```python
async def example_job(): # Your job logic here

wrapped_job = wrap("your_job_key", example_job)
await wrapped_job()
# cronpulse-python
```
