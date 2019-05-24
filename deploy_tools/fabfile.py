import random
from string import ascii_letters
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = r'https://github.com/mukiblejlok/tdd-python-book.git'


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} . ')
    current_commit = local("git log -n 1 --format=%H",
                           capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('venv/bin/pip'):
        run(f'python3 -m venv venv')
    run('./venv/bin/pip install -r requirements.txt')


def _create_or_update_dotenv():
    append('.env', "DJANGO_DEBUG_FALSE=y")
    append('.env', f"SITENAME={env.host}")
    current_contents = run('cat .env')
    if "DJANGO_SECRET_KEY" in current_contents:
        return
    else:
        rg50 = random.choices(ascii_letters, k=50)
        new_secret = ''.join(rg50)
        append('.env', f"DJANGO_SECRET_KEY={new_secret}")


def _update_static_files():
    run('./venv/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./venv/bin/python manage.py migrate --noinput')

