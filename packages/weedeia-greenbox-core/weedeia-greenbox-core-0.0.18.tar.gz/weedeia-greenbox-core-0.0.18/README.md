### Development

```shell
python -m venv env
#pip install rpi.gpio only is supported

fastapi main.py
```

### Publish new version

First, update version in setup.py

```shell
pip install setuptools wheel twine build
python setup.py sdist bdist_wheel
twine upload dist/*
```
