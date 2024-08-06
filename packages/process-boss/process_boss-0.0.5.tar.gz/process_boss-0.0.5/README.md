# Process Boss
![Python CI Build](https://github.com/kristof9851/process_boss/actions/workflows/python-ci.yml/badge.svg)
![PyPI Downloads](https://img.shields.io/pypi/dm/process_boss?label=PyPI%20Downloads&color=rgb(50%2C%20165%2C%20233)
)

*A Cron job scheduler implemented in Python*

## 1. Installation

```bash
pip install process_boss
```

## 2. Usage
Create a configuration file in `config.yaml` somewhere on disk, then run process boss:

```bash
python -m process_boss ~/config.yaml
```

### Example: Run a script on Monday mornings

```yaml
processes:
  - id: test-job
    cron: "0 7 * * MON" # every Monday at 7:00 AM
    command: "echo 'Hello World!'"
```

## 3. Configuration reference

| Property | Required | Default | Description |
| -------- | ------- | -------- | ------- | 
| `scheduler.maxWorkers` | No | 10  | Each process is executed in a thread. This is the maximum number of  threads that should be used |
| `scheduler.loop.restartSeconds` | No | 15 | Number of seconds to wait before reading the config again and evaluating all processes' cron expressions |
| `scheduler.loop.runOnce` | No | False | If set to True, the processes in the config file will only be read and executed once, after that process_boss exits. |
| `logs.enabled` | No | False | If set to True, it enables logging of both the scheduler, and each execute process in a separate file. The below two are required to set if enabled. |
| `logs.schedulerLogDir` | No | "" | Absolute directory path where the log file of the scheduler can be created per each process. Contains metadata about when a given process will run next, and with what parameters. Eg: `/var/log/process_boss/scheduler` |
| `logs.processLogDir` | No | "" | Absolute directory path where the log file of each process can be created, one per execution. Contains the parameters used before ezecution, and the STDOUT and STDERR output of the process. Eg: `/var/log/process_boss/process` |
| `processes[].id` | Yes | - | Non-empty arbitrary string. Eg: `my-process` |
| `processes[].cron` | Yes | - | Non-empty string, should be a CRON expression. Eg. `0 7 * * MON` |
| `processes[].command` | Yes | - | Non-empty string, should be an executable command. Eg. `python script.py` |
| `processes[].runAtStartup` | No | False | If set to True, the process will be executed immediately when process_boss starts, instead of waiting for the next CRON match |

## 4. Maintainer documentation
See: [docs/README_MAINTAINER.md](docs/README_MAINTAINER.md)
