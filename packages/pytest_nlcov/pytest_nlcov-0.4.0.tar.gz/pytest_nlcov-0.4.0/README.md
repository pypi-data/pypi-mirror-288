# pytest_nlcov

With `pytest_nlcov` you can check the test coverage of new lines only. It will
check git for added and modified lines and will compute the coverage
just for those lines

## Installation

```sh
pip install pytest_nlcov
```

Note: `pytest_cov` is required and will be automatically installed when it
is not installed yet.

## Usage with pytest

When `pytest_nlcov` is installed, it will be discovered by pytest and executed as last step to
show you the test coverage of new lines.

```sh
pytest
```

Three options can be given:

- revision
- fail threshold
- root_dir

### Revision

Default, the new lines are based on the git diff with master. You can specify other revisions.

```sh
pytest --cov=myproj --nlcov-revision=main
```

### Fail Threshold

Optionally you can add a threshold to fail the tests when the coverage is below the threshold.

```sh
pytest --cov=myproj --nlcov-fail-under=0.6
```

### Root Dir

Optionally you can set the root dir of the git repo, so the command can be run from another directory that is
not the root of the repo.

```sh
pytest --cov=myproj --nlcov-root-dir=repo_dir
```


### Note
It's important to include `--cov` to load the **pytest_cov** plugin; otherwise an error message will appear saying:
> nlcov is installed, but pytest-cov is not installed, so nlcov will not be executed.


## Usage without pytest

`pytest_nlcov` can be run without pytest. Therefor you have to run `coverage` first, because `pytest_nlcov`
needs its coverage data.

```sh
coverage
nlcov
```

Optionally a revision can be given

```sh
nlcov main
```
