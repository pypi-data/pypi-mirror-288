# practice-poetry-project-release

### Prerequisites (Windows)
Recommended to install with the following steps.
- Python 3.10.x, 3.11.x or 3.12.x (binary distribution of [python.org](https://www.python.org/))
- Poetry Installtion to global
```
> pip install poetry
```

### Install alib dependencies
At the root directory,
```
$ poetry install
```
If it takes long time to finish poetry install, please try to set PYTHON_KEYRING_BACKEND as below.
```
$ PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring poetry install
```

## Enter virtual env. created by poetry
```sh
$ poetry shell
```