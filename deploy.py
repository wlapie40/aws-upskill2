import os
import subprocess
import time

#  todo in progress ^^
flask_env = os.environ.get('FLASK_ENV', False)
subprocess.run('pip --version')
try:
    subprocess.run('pipenv --version')
except:
    subprocess.run('pip install pipenv')

if flask_env:
    subprocess.run('pipenv install -r requirements.txt')
    print('======= generating creds for db =======')
    subprocess.run('python gen_creds_for_db.py')
    subprocess.run('docker-compose down')

    if flask_env == 'docker':
        subprocess.run('docker-compose -f docker-compose-docker.yml up -d --force-recreate --remove-orphans')
    elif flask_env == 'dev':
        subprocess.run('docker-compose up -d --force-recreate --remove-orphans')
    else:
        subprocess.run('docker-compose up -d')

    time.sleep(3)
    print('sleeping...')
    print('======= running flask =======')
    subprocess.run('python app.py')
else:
    raise KeyError('FLASK_ENV has not been set up :( ')