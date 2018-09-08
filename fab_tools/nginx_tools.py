'''
nginx fab tools
notice: the nginx installation is missing 
'''

from fab_tools import info
from fab_tools import Config
from fabric import task

_conf_repo_path = Config['git_repo_dist_path']+'/'\
                 +Config['nginx_conf_file_repo_path']
_conf_srv_path = Config['nginx_conf_file_srv_path']

@task
def start(c):
    info('Copy from '+_conf_repo_path+' to '+_conf_srv_path)
    c.sudo('cp '+_conf_repo_path+' '+_conf_srv_path, echo=True)
    info('Start nginx service')
    c.sudo('nginx', echo=True)


@task
def reload(c):
    info('Copy from '+_conf_repo_path+' to '+_conf_srv_path)
    c.sudo('cp '+_conf_repo_path+' '+_conf_srv_path, echo=True)
    info('reload nginx service')
    c.sudo('nginx -s reload', echo=True)
