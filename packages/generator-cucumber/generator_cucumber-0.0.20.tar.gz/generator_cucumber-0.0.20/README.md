# Cucmber generator

<div align="center"><img src="images/InnoLab.png" height="150" alt="Innovation lab"></div>

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
├── 📁 docs/                    #
|   ├── 📋 api.rst                  #
|   ├── 🐍 conf.py                  #
|   ├── 📋 index.rst                #
|   ├── 🎬 make.bat                 #
|   ├── 🎬 Makefile                 #
|   ├── 🐍 requirements.in          #
|   ├── 🐍 requirements.txt         #
|   └── 📋 usage.rst                #
├── 📁 example/
|   ├── 🐍 __init__.py          #
|   ├── ⚙️ pytest.ini               #
|   ├── 🥒 test_app.feature         # .feature файл (шаблон)
|   ├── 🐍 test_app                 # feature test (шаблон)
|   ├── 🐍 test_github.py           # Пример для github
|   └── 🐍 test_gitlab.py           # Пример для gitlab
├── 📁 generator_cucumber/      #
|   ├── 🐍 __init__.py              # иницилизация
|   ├── 🐍 api_github.py            # для работы с github (не реализован)
|   ├── 🐍 api_gitlab.py            # Для работы с gitlab
|   ├── 🐍 bdd_generator.py         # Для работы с .py и подготовка шаблона bdd
|   ├── 🐍 cache_file.py            # создание файлов cache
|   ├── 🐍 create_file.py           # Обработка файлов cache и .feature
|   ├── 🐍 cucumber_text.py         # Формирование .feature текст
|   └── 🐍 generator.py             # входная точка
├── 📁 images/
|   └── 📷 InnoLab.png              # лого проекта
├──  📋 .env                    # глобальные перменные
├──  📋 .gitignore              #
├──  🦊 .gitlab-ci.yml          #
├──  🎬 build_l.sh              # скрипт для publish на pypi
├──  🦊 container-builder.yml   #
├──  🎬 del_l.sh                # скрипт для удаление build проекта
├──  🐳 Dockerfile              # 
├──  📋 LICENSE                 #
├──  🐍 pyproject.toml          #
├──  📗 README_PY.md            # инструкция для pypi
├──  📘 README.md               # инструкция для git и локальной работы
├──  📘 README.rst              # иснтрукция readthedocs
├──  🦊 readthedocs.yml         #
├──  💾 requirements-test.txt   # lib для работы в example
├──  💾 requirements.txt        # lib для работы с generator_cucumber
├──  ⚙️ setup.cfg               #
└──  🐍 setup.py                #
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