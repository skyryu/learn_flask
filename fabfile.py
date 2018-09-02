'''
install fabric with pip
fab --list  #use this cmd to list all the tasks in $PWD/fabfile.py
fab -i /path/to/private_ssh_key_file -H user@public_domain_name task_name
'''

from fabric import task
from invoke import Responder, Exit
from invocations.console import confirm

INSTALL_RESPOND = Responder(pattern=r"Is this ok \[(Y|N|y|n)+.*]:.*",
                            response="y\n")
Config={
    #AWS EC2 config
    'ec2_usrname':'ec2-user',

    #conda config
    'conda_script_path':'~/anaconda.sh',
    'conda_install_path':'/etc/anaconda',
    'conda_version':'Anaconda2-5.2.0-Linux-x86_64.sh',

    #conda env config
    'env_name':'flask_py3',
    'env_dir_path':'/srv/dist/conda_env/flask_py3',
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
    install_anaconda(c)
    install_git(c)
    install_bower(c)

@task
def init_dist(c):
    '''
    First time code pulling for a new server
    '''
    if not confirm('make sure you have run deploy-dist'):
        raise Exit('aborting dist initialization')
    git_clone(c)
    create_virtual_env(c)
    bower_pkg_install(c)

@task
def update_dist(c):
    '''
    code/virtual_env/DB updating
    '''
    if not confirm('make sure you have run init-dist'):
        raise Exit('aborting dist updating')
    update_git_repo(c)
    update_virtual_env(c)
    update_bower_pkg(c)

def info(info_str):
    '''
    provide colorful terminal info output.
    '''
    INFO_COLOR = "\033[0;36m"
    INFO_END = "\033[0m"
    print(INFO_COLOR+'[INFO]'+info_str+INFO_END)

#Update and install cmd
@task
def update_git_repo(c):
    info('Start updating git repo')
    c.run('git pull', echo=True)

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
def update_virtual_env(c):
    info('Start updating conda env')
    c.sudo(Config['conda_install_path']+'/bin/conda env update'
           +' -n '+Config['env_name']
           +' -f='+Config['env_yaml_path'])

#tools installation cmd set
@task
def uninstall_anaconda(c):
    info('Start uninstalling the anaconda if already installed')
    if c.sudo('test -f '+Config['conda_script_path'], warn=True).ok:
        c.sudo('rm '+Config['conda_script_path'])
    if c.sudo('test -d '+Config['conda_install_path'], warn=True).ok:
        c.sudo('rm -rf '+Config['conda_install_path'])

@task
def install_anaconda(c):
    uninstall_anaconda(c)
    info('step1> Use wget to download Anaconda')
    c.sudo('wget https://repo.continuum.io/archive/'\
           +Config['conda_version']+' -O '+Config['conda_script_path'])

    info('step2> Run script to install anaconda')
    c.sudo('bash '+Config['conda_script_path']+' -b -p '\
            +Config['conda_install_path'])
    #c.run('export PATH="/etc/anaconda/bin:$PATH"')
    #c.run('source /etc/anaconda/bin/activate')

    info('step3> Anaconda installation finished. Clean up the temp script.')
    c.run('rm '+Config['conda_script_path'])

@task
def create_virtual_env(c):
    remove_virtual_env(c)
    info('Start creating conda env')
    c.sudo(Config['conda_install_path']+'/bin/conda env create'
           +' -n '+Config['env_name']
           +' -f='+Config['env_yaml_path']
           +' -p '+Config['env_dir_path'])

@task
def remove_virtual_env(c):
    info('Start removing conda env')
    if c.sudo('test -d '+Config['env_dir_path'], warn=True).ok:
        c.sudo('rm -rf '+Config['env_dir_path'])
        info(Config['env_dir_path']+' has been removed')

@task
def install_git(c):
    uninstall_git(c)
    info('Start installing git')
    #the pty flag enforce the terminal to print
    #the prompt line instead of buffering it.
    #So that we can do the watcher pattern  matching
    c.sudo('yum install git', pty=True,
           watchers=[Respond['git_(un)install_confirm']]
          )
    result = c.run('git --version', hide='out')
    info('git installation Done. Version:'+result.stdout.strip())

    info('Start setting up git config')
    c.run('git config --global user.name \"'+Config['git_username']+'\"')
    c.run('git config --global user.email \"'+Config['git_useremail']+'\"')

    if c.run('test -f '+Config['git_ssh_key_path'], warn=True).ok\
       and c.run('test -f '+Config['git_ssh_key_path']+'.pub', warn=True).ok:
        info('Rsa key already exists, skip key generation')
    else:
        info('Start generating ssh key')
        c.run('ssh-keygen -t rsa -C \"'+Config['git_useremail']+'\"',
              pty=True, watchers=[Respond['git_ssh_path_confirm'],
                                  Respond['git_passphrase']
                                 ]
             )
    ssh_result = c.run('ssh -T git@github.com', hide=True, warn=True)
    info('Key generation done. Try ssh\n{0}, exit code:{1}'.format(
        'stdout:'+ssh_result.stdout.strip()+'\nstderr:'+ssh_result.stderr.strip(),
        ssh_result.exited)
        )

@task
def uninstall_git(c):
    info('Start uninstalling git')
    result = c.sudo('yum remove git', pty=True,
                    watchers=[Respond['git_(un)install_confirm']]
                   )
    info('Uninstallation finished, exit code:'+str(result.exited))

@task
def git_clone(c):
    git_remove_repo(c)
    if c.run('test -d '+Config['git_repo_dist_path'], warn=True).failed:
        c.sudo('mkdir -p '+Config['git_repo_dist_path'])
        c.sudo('chown -R '+Config['ec2_usrname']+' '
               +Config['git_repo_dist_path'])
        info('Create git repo dir:'+Config['git_repo_dist_path'])
    info('clone git repo to:'+Config['git_repo_dist_path'])
    c.run('git clone {0} {1}'.format(Config['github_repo_url'],
                                     Config['git_repo_dist_path']))

@task
def git_remove_repo(c):
    info('Start removing git repo if exists')
    if c.run('test -d '+Config['git_repo_dist_path'], warn=True).ok:
        c.sudo('rm -rf '+Config['git_repo_dist_path'], echo=True)

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




