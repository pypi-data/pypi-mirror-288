from .api_gitlab import Gitlab_api
from .api_github import GitHub_api

class Generator:
    def __init__(self, URL_GIT, PRIVATE_TOKEN_GIT):
        self.URL_GIT = URL_GIT
        self.PRIVATE_TOKEN_GIT = PRIVATE_TOKEN_GIT

    def create_cucumber(**params):
        try:
            issue_github_id = params['issue_github_id']
            owner = params['owner']
            repo = params['repo']
        except:
            issue_github_id = False
            owner = False
            repo = False

        try:
            generator = params['generator']
        except KeyError:
            generator = False
        try:
            all_epic = params['all_epic']
        except KeyError:
            all_epic = True
        try:
            allure = params['allure']
        except KeyError:
            allure = False

        # GITLAB
        if owner == False and repo == False:
            Gitlab_api.URL_GIT = Generator.URL_GIT
            Gitlab_api.PRIVATE_TOKEN_GIT = Generator.PRIVATE_TOKEN_GIT
        # GROUP
            try:
                ssl_verify = params['ssl_verify']
            except KeyError:
                ssl_verify = False
            try:
                group_id = params['group_id']
                epi_iid = params['epi_iid']
            except KeyError:
                group_id = False
                epi_iid =False

            try:
                project_id = params['project_id']
                issue_iid = params['issue_iid']
            except KeyError:
                project_id = False
                issue_iid = False

            Gitlab_api.create_cucumber(
                project_id=project_id,
                issue_iid=issue_iid,

                group_id=group_id,
                epi_iid=epi_iid,

                name_file=params['name_file'],
                scenario_number=params['scenario_number'],
                generator=generator,
                allure=allure,
                all_epic=all_epic,
                ssl_verify=ssl_verify
            )

        # GITHUB
        else:
            GitHub_api.URL_GIT = Generator.URL_GIT
            GitHub_api.PRIVATE_TOKEN_GIT = Generator.PRIVATE_TOKEN_GIT
            GitHub_api.create_cucumber(
                issue_github_id=issue_github_id,
                owner=owner,
                repo=repo,

                name_file=params['name_file'],
                scenario_number=params['scenario_number'],
                generator=generator,
                all_epic=all_epic,
            )