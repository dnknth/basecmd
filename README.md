# basecmd

Logging boilerplate for the command line.

Classes inheriting from `BaseCmd` get a `self.log` attribute — a standard
Python `logging.Logger` — pre-configured to `sys.stdout` with color support
when logging to a terminal.

## Quick start

```python
from basecmd import BaseCmd


class MyCmd(BaseCmd):
    "Demo command"

    def add_arguments(self):
        self.parser.add_argument("--foo", help="Custom option")

    def __call__(self):
        self.log.debug("options: %s", self.options)


if __name__ == "__main__":
    cmd = MyCmd()
    cmd()
```

Run with `-h` / `--help` to see the built-in logging options:

```
usage: __main__.py [-h] [-v {error,warning,info,debug}] [--log-file LOG_FILE]
                   [--foo FOO]
```

## Configuration

Defaults can be set via environment variables or a `.env` file:

| Variable | Description | Default |
|---|---|---|
| `LOG_LEVEL` | Logging verbosity: `error`, `warning`, `info`, or `debug` | `info` |
| `LOG_FILE` | Path to a log file; stdout when unset | `None` (stdout) |
| `LOG_FORMAT` | Python `logging` format string | unset → `%(asctime).19s  %(message)s` |
