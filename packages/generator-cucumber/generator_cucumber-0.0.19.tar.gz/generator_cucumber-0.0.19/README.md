# Cucmber generator

<div align="center"><img src="https://gitlab.com/python_lib/generator_cucumber/-/blob/main/images/InnoLab.png?ref_type=heads" height="150" alt="Innovation lab"></div>

### Venv (Linux/Mac)
```bash
# add venv
python3.8 -m venv .venv
# activate venv
. .venv/bin/activate
# install lib
pip3 install -r requirements.txt
# update pip
pip install --upgrade pip
```

### Venv (Windows)
```bash
# add venv
python -m venv .venv
# activate venv
.venv\Scripts\activate
# install lib
pip3 install -r requirements.txt
# exit venv
deactivate
```

### Structure
```
# Создаем страницу Login
├── 📁 docs/
|   ├── 📋 api.rst
|   ├── 🐍 conf.py
|   └── ...  
├── 📁 example/
|   ├── 🐍 __init__.py
|   ├── 🐍 generator.py
|   └── ...  
├── 📁 generator_cucumber/
|   ├── ⚙️ pytest.ini
|   ├── 💾 requirements.txt
|   ├── 🥒 test_app.feature
|   ├── 🐍 test_app.py
|   ├── 🐍 test_generator.py
|   └── ...  
├── 📁 images/
|   └── 📷 InnoLab.png
├──  📋 .env
├──  📋 .gitignore
├──  📋 LICENSE
├──  📗 README_PY.md
├──  📘 README.md
├──  💾 requirements.txt
├──  ⚙️ setup.cfg
└──  🐍 setup.py  
```

### Lib for build 
```bash
# setuptools
pip3 install setuptools
# twine
pip3 install twine
# build
pip3 install build
```

### Public lib pip
```bash
pyproject-build && twine upload --skip-existing dist/*
```
 
### Information
[Создание библиотеки Python: полный гайд](https://habr.com/ru/articles/760046/)  
[Example projects readthedocs](https://docs.readthedocs.io/en/stable/examples.html)  
[Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)  
[Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)  