import gitlab
from .create_file import create_cucumber_file

class Gitlab_api:
    def __init__(self, URL_GIT, PRIVATE_TOKEN_GIT):
        self.URL_GIT = URL_GIT
        self.PRIVATE_TOKEN_GIT = PRIVATE_TOKEN_GIT

    def create_cucumber (**params):
        # Gitlab connect
        gl = gitlab.Gitlab(
            Gitlab_api.URL_GIT,
            private_token=Gitlab_api.PRIVATE_TOKEN_GIT,
            api_version=4,
            ssl_verify=params['ssl_verify']
        )
    # GROUP
        group_id = params['group_id']
        epi_iid = params['epi_iid']
        project_id = params['project_id']
        issue_iid = params['issue_iid']

        if group_id and epi_iid:
            group_id = params['group_id']
            group = gl.groups.get(group_id)
            # EPIC
            epi_iid = params['epi_iid']
            data_gitlab = group.epics.get(epi_iid)

        if project_id and issue_iid:
            project = gl.projects.get(params['project_id'])
            # ISSUE
            data_gitlab = project.issues.get(params['issue_iid'])

        # Создаем файл .feature
        create_cucumber_file(
            # Заголовок issue и еріс
            title=data_gitlab.title,
            # url issue и еріс из которого формируется .feature
            web_url=data_gitlab.web_url,
            # дата обновления issue и еріс для фиксации изменений
            updated_at=data_gitlab.updated_at,
            # автор issue и еріс
            author=data_gitlab.author['name'],
            # все содержимое, сам issue и еріс
            description=data_gitlab.description,
            # наименование файла .feature
            name_file=params['name_file'],
            # номер по которому формируется feature (внутри issue и еріс, например <scr-3-1>)
            scenario_number=params['scenario_number'],
            # работа с измнениеми только в блоке <scr-3-1><scr-3-1> или со всем issue и еріс. (True/False)
            all_epic=params['all_epic'],
            # для генерации теста из .feature в .ру
            generator=params['generator'],
            # добавить allure в код
            allure=params['allure']
        )