from config import conf
import os
from subprocess import Popen
from subprocess import PIPE

def wrapper_change_path(func):
    cwd = os.getcwd()

    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    os.chdir(cwd)
    return inner


class GitLog:
    commands = {
        'meta': 'meta_cmd',
        'numstat': 'numstat_cmd',
        'namestat': 'namestat_cmd',
        'merge_numstat': 'merge_numstat_cmd',
        'merge_namestat': 'merge_namestat_cmd'
    }

    def __init__(self):
        self.meta_cmd = 'git log --reverse --all --pretty=format:\"commit: %H%n' \
                        'parent: %P%n' \
                        'author: %an%n' \
                        'author email: %ae%n' \
                        'time stamp: %at%n' \
                        'committer: %cn%n' \
                        'committer email: %ce%n' \
                        '%B%n\"'
        self.numstat_cmd = 'git log --pretty=format:\"commit: %H\" --numstat --all --reverse'
        self.namestat_cmd = 'git log --pretty=format:\"commit: %H\" --name-status --all --reverse'
        self.merge_numstat_cmd = 'git log --pretty=oneline --numstat -m --merges --all --reverse'
        self.merge_namestat_cmd = 'git log --pretty=oneline  --name-status -m --merges --all --reverse'

    @wrapper_change_path
    def run(self, project):
        target_path = conf.project_path(project)
        os.chdir(target_path)
        for cmd_name in GitLog.commands.keys():
            print(cmd_name)
            cmd = getattr(self, GitLog.commands.get(cmd_name))
            log_path = conf.project_log_path(project, cmd_name)
            with open(log_path, 'wb') as log:
                with Popen(cmd, stdout=PIPE) as proc:
                    log.write(proc.stdout.read())



if __name__ == '__main__':
    projects = conf.projects
    for p in projects:
        GitLog().run(p)



