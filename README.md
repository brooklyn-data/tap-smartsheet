# Brooklyn Data Co's tap-smartsheet

`tap-smartsheet` is a Singer tap for Smartsheet.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

```bash
pipx install git+https://github.com/brooklyn-data/tap-smartsheet.git
```

## Configuration

### Accepted Config Options

Retrieve your access token following the instructions here: https://smartsheet-platform.github.io/api-docs/#raw-token-requests

Set the config key `smartsheet_access_token` with the value.

## Usage

You can easily run `tap-smartsheet` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-smartsheet --version
tap-smartsheet --help
tap-smartsheet --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-smartsheet --version
# OR run a test `elt` pipeline:
meltano elt tap-smartsheet target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
