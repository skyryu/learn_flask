'''
bower fab tools
'''

from fab_tools import info
from fab_tools import Config
from fabric import task


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

