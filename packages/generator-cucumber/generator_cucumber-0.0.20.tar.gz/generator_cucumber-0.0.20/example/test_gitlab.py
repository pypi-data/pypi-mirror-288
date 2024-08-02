import sys
import os
sys.path.append('..')
from dotenv import load_dotenv, find_dotenv

from generator_cucumber import Generator

load_dotenv(find_dotenv())
URL_GIT_LAB = os.environ.get('URL_GIT_LAB')
PRIVATE_TOKEN_GIT_LAB = os.environ.get('PRIVATE_TOKEN_GIT_LAB')

Generator.URL_GIT = URL_GIT_LAB
Generator.PRIVATE_TOKEN_GIT = PRIVATE_TOKEN_GIT_LAB

Generator.create_cucumber(
    project_id='59216833',
    issue_iid=1,
    name_file='test_gitlab',
    scenario_number='src-1-1',
    ssl_verify=True,
    allure=True
)