import sys
import os
sys.path.append('..')
from dotenv import load_dotenv, find_dotenv

from generator_cucumber import Generator

load_dotenv(find_dotenv())
URL_GIT_HUB = os.environ.get('URL_GIT_HUB')
PRIVATE_TOKEN_GIT_HUB = os.environ.get('PRIVATE_TOKEN_GIT_HUB')

Generator.URL_GIT = URL_GIT_HUB
Generator.PRIVATE_TOKEN_GIT = PRIVATE_TOKEN_GIT_HUB

Generator.create_cucumber(
    issue_github_id=1,
    name_file='test_github',
    scenario_number='src-1-1',
    owner="DemonDis",
    repo="bdd_generator"
)