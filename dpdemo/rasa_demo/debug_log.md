# pykwalify.errors.RuleError
## message
```
...
  File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/pykwalify/rule.py", line 438, in init
    raise RuleError(
pykwalify.errors.RuleError: <RuleError: error code 4: Unknown key: nullable found: Path: '/mapping;regex/.+'>
```

## solution
use the `pyproject.toml` and `poetry.lock` files from `rasa`, so to upgrade `pykwalify` to `1.8.0`, to support key `nullable`


# tensorflow - numpy error

## message
NotImplementedError: Cannot convert a symbolic Tensor (lstm_2/strided_slice:0) to a numpy array. T

## solution
modifying tensorflow/python/framework/ops.py

> NOTE: should modify the system `tensorflow `package, though using `rasa init` in venv, which is strange.

at line #845~846

FROM
```python
  def __array__(self):
    raise NotImplementedError(
```
TO
```python
  def __array__(self):
    raise TypeError(
```

https://stackoverflow.com/questions/66207609/notimplementederror-cannot-convert-a-symbolic-tensor-lstm-2-strided-slice0-t/66207610
