from dotenv import load_dotenv, dotenv_values
import jesse.helpers as jh
import os
import sys

# fix directory issue
sys.path.insert(0, os.getcwd())

ENV_VALUES = {}

if jh.is_jesse_project():
    # load env
    load_dotenv()

    # create and expose ENV_VALUES
    ENV_VALUES = dotenv_values('.env')
    
    if os.environ.get('POSTGRES_HOST', None):
        ENV_VALUES['POSTGRES_HOST'] = os.getenv('POSTGRES_HOST')
        ENV_VALUES['POSTGRES_NAME'] = os.getenv('POSTGRES_NAME')
        ENV_VALUES['POSTGRES_PORT'] = os.getenv('POSTGRES_PORT')
        ENV_VALUES['POSTGRES_USERNAME'] = os.getenv('POSTGRES_USERNAME')
        ENV_VALUES['POSTGRES_PASSWORD'] = os.getenv('POSTGRES_PASSWORD')
        ENV_VALUES['REDIS_HOST'] = os.getenv('REDIS_HOST')
        ENV_VALUES['REDIS_PORT'] = os.getenv('REDIS_PORT')
        ENV_VALUES['PASSWORD'] = os.getenv('JESSE_PASSWORD', 'unset')
        ENV_VALUES['REDIS_DB'] = 0


    if jh.is_unit_testing():
        ENV_VALUES['POSTGRES_HOST'] = '127.0.0.1'
        ENV_VALUES['POSTGRES_NAME'] = 'jesse_db'
        ENV_VALUES['POSTGRES_PORT'] = '5432'
        ENV_VALUES['POSTGRES_USERNAME'] = 'jesse_user'
        ENV_VALUES['POSTGRES_PASSWORD'] = 'password'
        ENV_VALUES['REDIS_HOST'] = 'localhost'
        ENV_VALUES['REDIS_PORT'] = '6379'
        ENV_VALUES['REDIS_DB'] = 0
        ENV_VALUES['REDIS_PASSWORD'] = ''

    # validation for existence of .env file
    if len(list(ENV_VALUES.keys())) == 0:
        jh.error(
            '.env file is missing from within your local project. '
            'This usually happens when you\'re in the wrong directory. '
            '\n\nIf you haven\'t created a Jesse project yet, do that by running: \n'
            'jesse make-project {name}\n'
            'And then go into that project, and run the same command.',
            force_print=True
        )
        os._exit(1)
        jh.terminate_app()
        # raise FileNotFoundError('.env file is missing from within your local project. This usually happens when you\'re in the wrong directory. You can create one by running "cp .env.example .env"')

    if not jh.is_unit_testing() and ENV_VALUES['PASSWORD'] == '':
        raise EnvironmentError('You forgot to set the PASSWORD in your .env file')
