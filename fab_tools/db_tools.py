'''
db fab tools
'''

from fab_tools import info
from fab_tools import Config
from fabric import task



@task
def upgrade(c):
    info('Start upgrade SQLAlchemy DB')
    c.run('source /etc/anaconda/bin/activate '+Config['env_dir_path']
          +' && cd '+Config['git_repo_dist_path']
          +' && python manage.py db upgrade', echo=True)


