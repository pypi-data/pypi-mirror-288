import requests
import os
from .create_file import create_cucumber_file

class GitHub_api:
    def __init__(self, URL_GIT, PRIVATE_TOKEN_GIT):
        self.URL_GIT = URL_GIT
        self.PRIVATE_TOKEN_GIT = PRIVATE_TOKEN_GIT
        
    def create_cucumber (**params):
    # GROUP
        token = os.getenv('GITHUB_TOKEN', GitHub_api.PRIVATE_TOKEN_GIT)
        owner = params['owner']
        repo = params['repo']
        issue_github_id = params['issue_github_id']
        query_url = f"{GitHub_api.URL_GIT}/{owner}/{repo}/issues/{issue_github_id}"
        param_obj={}
        headers = {'Authorization': f'token {token}'}
        r = requests.get(query_url, headers=headers, params=param_obj)

        data_gitlhub = r.json()

        # Создаем файл .feature
        create_cucumber_file(
            # Заголовок issue
            title=data_gitlhub['title'],
            # url issue из которого формируется .feature
            web_url=data_gitlhub['html_url'],
            # дата обновления issue для фиксации изменений
            updated_at=data_gitlhub['updated_at'],
            # автор issue
            author=data_gitlhub['author_association'],
            # все содержимое, сам issue
            description=data_gitlhub['body'],
            # наименование файла .feature
            name_file=params['name_file'],
            # номер по которому формируется feature (внутри issue, например <scr-3-1>)
            scenario_number=params['scenario_number'],
            # работа с измнениеми только в блоке <scr-3-1><scr-3-1> или со всем issue. (True/False)
            all_epic=params['all_epic'],
            # для генерации теста из .feature в .ру
            generator=params['generator']
        )