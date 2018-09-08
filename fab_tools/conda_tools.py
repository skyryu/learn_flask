'''
conda fab tools
'''
from fab_tools import info
from fab_tools import Config
from fabric import task

@task
def update_deploy_env(c):
    info('Start updating conda env:deploy_py2')
    c.sudo(Config['conda_install_path']+'/bin/conda env update'
           #+' -n '+Config['env_name'] #the -n will override the -p
           +' -f='+Config['deploy_env_yaml_path']
           +' -p '+Config['deploy_env_path'])

@task
def update_virtual_env(c):
    info('Start updating conda env')
    c.sudo(Config['conda_install_path']+'/bin/conda env update'
           #+' -n '+Config['env_name'] #the -n will override the -p
           +' -f='+Config['env_yaml_path']
           +' -p '+Config['env_dir_path'])


@task
def create_deploy_env(c):
    remove_deploy_env(c)
    info('Start creating conda env:deploy_py2')
    c.sudo(Config['conda_install_path']+'/bin/conda env create'
           #+' -n '+Config['env_name']
           +' -f='+Config['deploy_env_yaml_path']
           +' -p '+Config['deploy_env_path'])


@task
def remove_deploy_env(c):
    info('Start removing conda env:deploy_py2')
    if c.sudo('test -d '+Config['deploy_env_path'], warn=True).ok:
        c.sudo('rm -rf '+Config['deploy_env_path'])
        info(Config['deploy_env_path']+' has been removed')


@task
def create_virtual_env(c):
    remove_virtual_env(c)
    info('Start creating conda env')
    c.sudo(Config['conda_install_path']+'/bin/conda env create'
           #+' -n '+Config['env_name']
           +' -f='+Config['env_yaml_path']
           +' -p '+Config['env_dir_path'])

@task
def remove_virtual_env(c):
    info('Start removing conda env')
    if c.sudo('test -d '+Config['env_dir_path'], warn=True).ok:
        c.sudo('rm -rf '+Config['env_dir_path'])
        info(Config['env_dir_path']+' has been removed')


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
