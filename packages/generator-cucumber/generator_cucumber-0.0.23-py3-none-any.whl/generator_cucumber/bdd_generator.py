import sys 

# В стадии разработки !!!

bdd_words = [
    'Background:', 'Scenario:', 'Scenario Outline:',
    'Given', 'And', 'When', 'Then',
    'And', 'But', 'Rule', 'Examples:' 
]

def generator(**params):
    name_file = sys.argv[0]
    print(f'\n🤖 Активация генерации теста 🐍{name_file} 🤖\n')

    # берем тектс из .feature
    with open(f'./{params["name_file"]}.feature', 'r', encoding="utf-8") as feature_file:
        # txt_feature = feature_file.read()

        # берем и обрабатываем текст из test (.py)
        with open(f'./{name_file}', 'r+') as test_file:
            txt_test = test_file.read()

            import_bdd_words = 'then, scenario, scenarios, given, when'

            test_file.seek(0,0)
            test_file.write(f'"""{params["title"]}"""\n')
            test_file.write(f'import pytest\n')
            test_file.write(f'from pytest_bdd import ({import_bdd_words})\n')
            test_file.write(txt_test)
            # pos = txt_test.find('epi iid' )
            # test_file.seek(pos,0)

            # print(f'\n\n{pos}\n')
            # print(f'\n {cache_file_read.read()}\n').

            # list words = ['scenario', 'scenarios', 'given', "when','then']

            number = 1

            for i in feature_file.readlines():
                if 'Scenario' in i:
                    print(i)
                    scenario = i.replace("    Scenario: ", "").replace("\n", "")
                    test_file.write(
                        f'\n\n@scenario ("{params["name_file"]}.feature", "{scenario}")\n'
                        f'def test_{number}():\n    pass'
                    )

                if 'Then' in i:
                    print(i)
                    then = i.replace("        Then ", "").replace("\n", "").replace("<", "{").replace(">", "}")

                    test_file.write(
                        f"\n\n@then('{then}')\n"
                        f'def test_{number}():\n    pass'
                    )

                if 'When' in i:
                    print (i)
                    when = i.replace("        When ", "").replace("\n", "").replace("<", "{").replace(">", "}")

                    test_file.write(
                        f"\n\n@when('{when}')\n"
                        f'def test_{number}():\n    pass'
                    )

                if 'Given' in i:
                    print(i)
                    given = i.replace("        Given ", "").replace("\n", "").replace("<", "{").replace(">", "}")

                    test_file.write(
                        f"\n\n@given('{given}')\n"
                        f'def test_{number}():\n    pass'
                    )

        # pos = txt_test.find( epi iid')
        # print(f(\n\n{txt_feature}\n\n')

