import os
import difflib 
from simple_term_menu import TerminalMenu 

from bs4 import BeautifulSoup
from .cucumber_text import create_cucumber_text
from .cache_file import feature_cache_file, changes_cache_file
from .bdd_generator import generator
from .allure_generator import allure_import

# создаем файл .feature и cache.txt
def create_cucumber_file(**params):

    # проверяем наличие папки под __featurecache__
    if os.path.isdir("__featurecache__") != True:
        os.mkdir("__featurecache__")
        os.mkdir("__featurecache__/feature_cache")
        os.mkdir("__featurecache__/feature_cache_changes")

    # меню выбора при измение в еріс
    options = [
        f'🔴 обновить  🥒 {params["name_file"]}.feature',
        f'🔵 не менять 🥒 {params["name_file"]}.feature',
    ]
    soup = BeautifulSoup(str(params["description"]), 'html.parser')

    if params["all_epic"] == True:
        description_html = params["description"]
    else:
        description_html = soup.find(params["scenario_number"])

    # проверяем создан ли файл
    if os.path.isfile(f'{params["name_file"]}.feature'):
        print('\n⛔ Такой 🥒 уже есть 👉', f'{params["name_file"]}.feature')
        file = open(f'{params["name_file"]}.feature')
    
        # записываем дату обновления
        file_date = file.readlines()[2].replace("# ", "").replace("\n", "")
        updated_at = params["updated_at"]

        # Сравниваем дату последнего обновления в локальном txt и epic gitlab
        if file_date == updated_at:
            print(f'🔵 Текст НЕ менялся')
        else:
            print(f'🔴 Текст менялся\n')

            # сравниваем локальный файл (txt) с еріс
            cache_file_read = open(f'__featurecache__/feature_cache/{params["name_file"]}.txt', 'r')
            cache_text = f"""{cache_file_read.read()}"""
            epic_text = f"""{description_html}"""

            diff = difflib.ndiff(cache_text.splitlines(), epic_text.splitlines())
            
            # показываем только изменения в epic
            print(f'➖➖➖➖ Изменения в тексте ➖➖➖➖')
            changes_diff = '\n'.join(line for line in diff if not line.startswith('  '))
            print(changes_diff)
            print(f'➖➖➖➖        END       ➖➖➖➖\n')

            # вывод терминального меню
            terminal_menu = TerminalMenu(options)
            menu_entry_index = terminal_menu.show()
     
            # если согласились на изменения => обновлением .feature и записываем изменения в cache txt
            if menu_entry_index == 0:
                # cache еріс для фиксации изменений
                feature_cache_file(**params, description_html=description_html)
                # формирование текста
                create_cucumber_text(**params)

                if params['generator'] == True:
                    generator(**params)

                print(f'⛔ Файл {params["name_file"]}.feature изменен ⛔')
                # фиксируем изменения в .txt с датоай
                changes_cache_file(**params, changes_diff=changes_diff)
            else:                
                print(f'🔵 Отмена обновлений файла {params["name_file"]}.feature 🔵')
    else:
        # формирование текста
        create_cucumber_text(**params)
        
        # проверяем создан ли файл cache_changes
        if os.path.isfile(f'__featurecache__/feature_cache/{params["name_file"]}.txt'):
            print('\n⛔ Такой 📁 уже есть 👉', f'__featurecache__/feature_cache/{params["name_file"]}.txt')
        else:
            # файла .feature нет, создаем
            feature_cache_file(**params, description_html=description_html)

        if params['generator'] == True:
            generator(**params)

    if params['allure'] == True:
        allure_import(**params)