'''
install fabric with pip
fab --list  #use this cmd to list all the tasks in $PWD/fabfile.py
fab -i /path/to/private_ssh_key_file -H user@public_domain_name task_name
'''

from fabric import task
from invoke import Responder, Exit
from invocations.console import confirm

from fab_tools import conda_tools as conda
from fab_tools import git_tools as git
from fab_tools import supervisor_tools as sup


INSTALL_RESPOND = Responder(pattern=r"Is this ok \[(Y|N|y|n)+.*]:.*",
                            response="y\n")
Config={
    #supervisor
    'pname':'dark_soul',

    #AWS EC2 config
    'ec2_usrname':'ec2-user',

    #conda config
    'conda_script_path':'~/anaconda.sh',
    'conda_install_path':'/etc/anaconda',
    'conda_version':'Anaconda2-5.2.0-Linux-x86_64.sh',

    #conda env config
    'env_name':'flask_py3',
    'env_dir_path':'/srv/dist/conda_env/flask_py3',
    'deploy_env_path':'srv/dist/conda_env/deploy_py2',
    'env_yaml_path':'/srv/dist/site/environment.yaml',
    'pip_conf_path':'~/.pip/pip.conf',

    #git config
    'git_username':'skyryu',
    'git_useremail':'skyryu@126.com',
    'git_ssh_key_path': "/home/ec2-user/.ssh/id_rsa",

    #git repo config
    'git_repo_dist_path': '/srv/dist/site',
    'github_repo_url':'git@github.com:skyryu/learn_flask.git',

    #bower config
    'bower_path':'/srv/dist/site/dark_soul/static',
}

Respond = {
    #git install responder
    'git_(un)install_confirm':INSTALL_RESPOND,
    'git_passphrase':Responder(
        pattern=r"Enter (same )*passphrase.*",
        response="\n"),
    'git_ssh_path_confirm':Responder(
        pattern=r"Enter file in which to save the key.*",
        response=Config['git_ssh_key_path']+"\n"),

    #bower install responder
    'npm_(un)install_confirm':INSTALL_RESPOND,
}


@task
def test(c):
    c.run('export PATH="$PATH:/etc/anaconda/bin"')
    c.run('source /etc/anaconda/bin/activate')

#All in One cmd set
@task
def deploy_dist(c):
    '''
    deploy a new server, install all tools
    '''
    if not confirm('the deployment will wipe out '
                   +'all the existing packages. Is this ok'):
        raise Exit('aborting dist deployment')
    conda.install_anaconda(c)
    git.install_git(c)
    install_bower(c)

@task
def init_dist(c):
    '''
    First time code pulling for a new server
    '''
    if not confirm('make sure you have run deploy-dist'):
        raise Exit('aborting dist initialization')
    git.git_clone(c)
    conda.create_virtual_env(c)
    bower_pkg_install(c)

@task
def update_dist(c):
    '''
    code/virtual_env/DB updating
    '''
    if not confirm('make sure you have run init-dist'):
        raise Exit('aborting dist updating')
    git.update_git_repo(c)
    conda.update_virtual_env(c)
    update_bower_pkg(c)
    upgrade_db(c)

def info(info_str):
    '''
    provide colorful terminal info output.
    '''
    INFO_COLOR = "\033[0;36m"
    INFO_END = "\033[0m"
    print(INFO_COLOR+'[INFO]'+info_str+INFO_END)

#Update and install cmd
@task
def bower_pkg_install(c):
    info('Start installing bower package')
    if c.sudo('test -d '+Config['bower_path']+'/bower_components', warn=True).ok:
        c.sudo('rm -rf '+Config['bower_path']+'/bower_components')
        info('remove existing bower_components')
    c.run('cd '+Config['bower_path']+' && bower install', echo=True)

@task
def update_bower_pkg(c):
    info('Start updating bower package')
    c.run('cd '+Config['bower_path']+' && bower install', echo=True)


@task
def upgrade_db(c):
    info('Start upgrade SQLAlchemy DB')
    c.run('source /etc/anaconda/bin/activate '+Config['env_dir_path']
          +' && cd '+Config['git_repo_dist_path']
          +' && python manage.py db upgrade', echo=True)

#tools installation cmd set

@task
def install_bower(c):
    uninstall_bower(c)
    info('Start installing bower')
    info('Step1>install node & npm')
    c.sudo('yum install nodejs npm --enablerepo=epel', pty=True,
           watchers=[Respond['npm_(un)install_confirm']])
    info('Step2>install bower')
    #turn off ssl check or you will get Error: UNABLE_TO_GET_ISSUER_CERT_LOCALLY
    c.sudo('npm config set strict-ssl false')
    c.sudo('npm install -g bower')
    info('bower installation done')

@task
def uninstall_bower(c):
    info('Start uninstalling bower and npm')
    c.sudo('npm uninstall bower')
    c.sudo('yum remove nodejs npm', pty=True,
           watchers=[Respond['npm_(un)install_confirm']])
    info('uninstallation done')




