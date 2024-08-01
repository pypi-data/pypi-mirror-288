📢🔬 xxy
========

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Release Building](https://github.com/iaalm/xxy/actions/workflows/release.yml/badge.svg)](https://github.com/iaalm/xxy/actions/workflows/release.yml)
[![PyPI version](https://badge.fury.io/py/xxy.svg)](https://badge.fury.io/py/xxy)

## Run
```shell
python -m xxy ./data_example -t "000002.SZ" -d 2023 -n "主营业务收入" -vv
```

### Config file
Config file is under `~/.xxy_cfg.json`.

## Development

### Install dependency
```shell
pip install -e .[dev]
```

### Lint
```shell
make format
```

### Log critiria
| Level | Verbosity | Frequency | Description |
|-------|-----------|-----------|-------------|
| Error | Always | Once per run |Something wrong, can't run anymore |
| Warning | Always | A few time per run |Something wrong, but can still run |
| Success | -v | At most once per run each line | User should easy to understand |
| Info | -vv | More than once per run each line | User should easy to understand |
| Debug | -vvv | At most three per second | Technical details for developers |
| Trace | -vvvv | More than three per second | Easy to know where code is hang |
