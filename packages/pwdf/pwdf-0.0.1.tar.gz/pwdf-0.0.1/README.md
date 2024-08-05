# pwdf
A terminal command (Python module) to get the path of a file (pwd for files instead of directories).

<br>

## Usage
`pwdf <relative file path>`

### Example:
```shell
foo@bar:~$ pwdf testfile.json
/Users/ryn/Documents/testfiles/testfile.json
```

<br>

## Building and Installing
**Test install:** `python setup.py install`

**Build distributions:** `python setup.py sdist bdist_wheel`

**Install distributions:** `pip install dist/pwdf-<version>-py2.py3-none-any.whl`