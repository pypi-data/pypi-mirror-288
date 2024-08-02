### Cucmber generator

Для формирования .feature файлов на основе html tags. 
Необходимую информацию для .feature файлов берем из epic/issue GitLab и GitHub.


### Установка

Вводим в терминал следующую команду
```bash
pip install generator-cucumber
```
или вносим в requirements.txt

```bash
generator-cucumber==0.0.20
```

### Пример работы generator-cucumber

1. Создаем epic и добавляем специальные tags (дублирующие ключевые слова языка Gherkin)

```<src-1>```  
```<src-1-1>```

```<scenario>```Напишем сценарий```</scenario>```  

```<given>```Здесь добавим given```</given>```  
```<when>```Здесь добавим when```</when>```  
```<then>```Здесь добавим then```</then>```  

```<group>```  

```<then>```Таблица THEN```<groupin>``` ```</groupin>``` ```</then>```

|Наименование                     |Что-то|
|---------------------------------|------|
|```<examples>```Первый```</examples>```      |1     |
|```<examples>```Второй```</examples>```      |2     |
|```<examples>```Третий```</examples>```      |3     |

```</group>```

```</src-1-1>```  
```</src-1>```  

2. В GitLab Epic будет выглядить следующим образом

<src-1>
<src-1-1>

<scenario>Напишем сценарий</scenario>  

<given>Здесь добавим given</given>  
<when>Здесь добавим when</when>  
<then>Здесь добавим then</then>  

<group>
<then>Таблица THEN <groupin></groupin></then>  

|Наименование                     |Что-то|
|---------------------------------|------|
|<examples>Первый</examples>      |1     |
|<examples>Второй</examples>      |2     |
|<examples>Третий</examples>      |3     |

</group>

</src-1-1>
</src-1>

3. После установки generator-cucumber создаем тест (например test_example.py)

```python
from generator_cucumber import Generator

Generator.URL_GIT = 'https://gitlab.com/' # url развернутого gitlab
Generator.PRIVATE_TOKEN_GIT = 'gsdff-sdx5DkswkqSDFSSQnVL' #'здесь необходим ваш access token (для примeра)

Generator.create_cucumber(
    group_id=100, # номер группы в которой написан epic
    epi_iid=1, # номер  epic
    name_file='test_lib', # наименование файла .feature (любое удобное)
    scenario_number='src-1-1', # текст к которому относиться тест
    ssl_verify=True # если все ок с ssl, по умолчанию false
)
```

3. После запуска теста сформируется .feature файл и папка __featurecache__ для контроля изменений в тексте 

```
# https://gitlab.com/python_epic/test_pr/-/epic/1
# Di
# 2024-08-01T01:48:53.366Z

Feature: Тестируем lib

    Scenario: Напишем сценарий

        Given Здесь добавим given

        When Здесь добавим when

        Then Таблица THEN  "<col_1>", "<col_2>", "<col_3>"
 
            Examples: col_1, col_2, col_3
                | col_1 | col_2 | col_3 |
                | Первый | Второй | Третий |
```

### Html tags
| gherkin equivalent |  HTML equivalent                           |
|--------------------|--------------------------------------------|
|"and"               |```<and></and>```                           |
|"background"        |```<background></background>```             |
|"but"               |```<but></but>```                           |
|"examples"          |```<examples></examples>```                 |
|"feature"           |```<feature></feature>```                   |
|"given"             |```<given></given>```                       |
|"scenario"          |```<scenario></scenario>```                 |
|"scenarioOutline"   |```<scenariooutline></scenariooutline>```   |
|"then"              |```<then></then>```                         |
|"when"              |```<when></when>```                         |

### Html tags ➕
| gherkin equivalent |  HTML equivalent (tags)                    | Описание                                                |
|--------------------|--------------------------------------------|---------------------------------------------------------|
|"groupin"           |```<groupin></groupin>```                   | Место куда поставиться examples                         |
|"scr-1-1"           |```<scr-1-1></scr-1-1>```                   | Для ограничения места для генерации (номер условный)    |

### Стуктура проекта
```
# Проект по генерации .feature
├── 📁 generator_cucumber/
|   ├── 🐍 api_github.py        # для работы с github (не реализован)
|   ├── 🐍 api_gitlab.py        # Для работы с gitlab
|   ├── 🐍 bdd_generator.py     # Для работы с .py и подготовка шаблона bdd
|   ├── 🐍 cache_file.py        # создание файлов cache
|   ├── 🐍 create_file.py       # Обработка файлов cache и .feature
|   ├── 🐍 cucumber_text.py     # Формирование .feature текст
|   └── 🐍 generator.py         # входная точка
└── ... 
```