## packaging

```bash
python setup.py sdist bdist_wheel
```

* After you run the command, it will create build and dist folders.
* And there is a whl file under the dist folder
* pip install the whl file

```bash
pip install dist/[package-filename].whl
```

* After that, you can now import the library and make use of it in your code

```bash
from xxxx import hello
hello()
```
