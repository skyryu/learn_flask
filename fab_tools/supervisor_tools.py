'''
'''

from fabric import task

@task
def start(c):
    c.sudo('source '+Config['conda_install_path']
           +'/bin/activate '+Config['deploy_env_path']
           +' && supervisord -c '+Config['git_repo_dist_path']
           +'/supervisord.conf', echo=True)

@task
def restart(c):
    c.sudo('source '+Config['conda_install_path']
           +'/bin/activate '+Config['deploy_env_path']
           +' && supervisorctl stop all && supervisorctl start all'
           +' -c ' +Config['git_repo_dist_path'] +'/supervisord.conf', echo=True)
