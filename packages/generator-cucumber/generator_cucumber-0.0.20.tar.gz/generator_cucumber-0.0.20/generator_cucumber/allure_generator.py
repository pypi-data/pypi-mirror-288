import os

# В стадии разработки !!!

def allure_import(**params):
    # настройка pytest.ini
    if os.path.isdir("pytest.ini"):
        with open('pytest.ini', 'r+') as pytest_file:
            # pytest_file.seek(0,0)
            # pytest_file = open('pytest.ini', 'a+')
            # pytest_file.writelines("Привет, файл!")
            
            pytest_file.writelines(
                f"@allure.epic('')\n"
            )

    else:
        # pytest_file.seek(0,0)
        pytest_file = open('pytest.ini', 'w+')

    # настройка requirements.txt
    # if os.path.isdir("requirements.txt"):
    #     with open('requirements.txt', 'r+') as pytest_file:
    #         pytest_file.write(f'import pytest\n')
    # else:
    #     pytest_file = open('pytest.py', 'w+')









        # pytest_file.writelines("import allure")
        # pytest_file.writelines(
        #     f"@allure.epic('')\n"
        #     f"@allure.feature('')\n"
        #     f"@allure.story('')\n"
        #     f"@allure.title('')\n"
        #     f"@allure.severty(allure.severity_level.NORMAL)\n"
        #     f"@allure.tag('')\n"
        #     f"@allure.description('')\n"
        # )
        # pytest_file.writelines(
        #     f"@allure.dynamic.parameter('Рабочая область', os.getcwd(), excluded=True)\n"
        #     f"@allure.dynamic.link('http', name=''name)\n"
        #     f"with allure.step('Шаги'):\n"
        #     f"  allure.attach('JSON', name='JSON', attacmnet_type=allure.attachment_type.TEXT):\n"
        # )







        # pytest_file.writelines("allure-pytest==2.12.0")
        # pytest_file.writelines("allure-python-commons==2.12.0")
