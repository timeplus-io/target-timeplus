# target-timeplus

`target-timeplus` is a Singer target for Timeplus.

Build with the [Meltano Target SDK](https://sdk.meltano.com).

## Installation

Install from PyPi (not ready in PyPi yet):

```bash
pipx install target-timeplus
```

Install from GitHub:

```bash
pipx install git+https://github.com/timeplus-io/target-timeplus.git@main
```


## Configuration

### Accepted Config Options

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| endpoint            | True     | https://us.timeplus.cloud/wsId1234 | Timeplus workspace endpoint |
| apikey              | True     | None    | Personal API key |
| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |
| flattening_enabled  | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth| False    | None    | The max depth to flatten schemas. |

A full list of supported settings and capabilities for this
target is available by running:

```bash
poetry run target-timeplus --about
```

### Configure using environment variables

This Singer target will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Target Authentication and Authorization

You need to create a free account at https://timeplus.com. Sign up with a Google or Microsoft ID, then create a new workspace with a random ID and a friendly name. Then you will be redirected to https://us.timeplus.cloud/wsId1234/console 

You need to create an API key to access Timeplus REST API. To do so:

1. Click the user icon on the top-right corner.
2. Choose Personal Settings
3. Choose the 2nd tab API Key Management
4. Click the Create API Key button
5. Set a readable name and choose an expiration date
6. Save the API key securely in your computer. You are not going to retrieve the plain text key again in the console.

For more details, please check https://docs.timeplus.com/docs/quickstart-ingest-api 

## Usage

You can easily run `target-timeplus` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Target Directly

```bash
poetry run target-timeplus --version
poetry run target-timeplus --help
# Test using the "tap-smoke-test" sample:
meltano elt tap-smoke-test target-timeplus
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `target_timeplus/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `target-timeplus` CLI interface directly using `poetry run`:

```bash
poetry run target-timeplus --help
```

### Testing with [Meltano](https://meltano.com/)

_**Note:** This target will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

<!--
Developer TODO:
Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in
the file.
-->

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd target-timeplus
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke target-timeplus --version
# OR run a test `elt` pipeline with the "tap-smoke-test" sample:
meltano elt tap-smoke-test target-timeplus
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the Meltano Singer SDK to
develop your own Singer taps and targets.
