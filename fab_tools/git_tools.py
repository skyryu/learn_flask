'''
git fab tools
'''

from fab_tools import info
from fab_tools import Config
from fabric import task

@task
def update_git_repo(c):
    info('Start updating git repo')
    c.run('cd '+Config['git_repo_dist_path']+' && git pull', echo=True)

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
