from __future__ import unicode_literals, print_function

import os
import re

from services.utils import execute, get_command_output


PKEY_PATH = os.environ.get('PRIVATE_KEY_PATH')
REPOSITORY_URI = 'git@bitbucket.org:spotmentordev/{name}.git'

GIT_CLONE_COMMAND = "ssh-agent ash -c 'ssh-add {}; ".format(PKEY_PATH) +\
    "git clone --single-branch -b {branch} {repo_uri} " +\
    "/var/lib/repo/{repo_name}'"

GIT_PULL_COMMAND = "ssh-agent ash -c 'ssh-add {}; ".format(PKEY_PATH) +\
    "git pull origin {branch}'"

GIT_COMPARE_COMMAND = 'git log --right-only --graph ' \
                      '--pretty=format:"%h    %an    %s" {left}...{right}'


def clone(repo, branch):
    repo_uri = REPOSITORY_URI.format(name=repo)

    command = GIT_CLONE_COMMAND.format(
        repo_uri=repo_uri, branch=branch, repo_name=repo)

    exit_code = execute(command)

    if exit_code:
        raise Exception('git clone failed with '
                        'exit code: {}'.format(exit_code))


def pull(branch):
    command = GIT_PULL_COMMAND.format(branch=branch)
    exit_code = execute(command)

    if exit_code:
        raise Exception('git pull failed with '
                        'exit code: {}'.format(exit_code))


def commit_diff(commit):
    command = GIT_COMPARE_COMMAND.format(left=commit, right='HEAD')
    output = get_command_output(command)

    # check if error in command
    if type(output) is tuple:
        output, code = output
        raise Exception('git log failed with '
                        'exit code: {}'.format(code))

    return output.decode()


def chdir(path):
    os.chdir(path)


def exists(path):
    return os.path.exists(path)


def parse_commit_diff(diff):
    diff = diff.strip()
    seperator = re.compile('\s{4}')

    if not diff:
        return []

    rows = diff.split('\n')

    commits = []
    for row in rows:
        sep = re.split(seperator, row, maxsplit=2)
        _id = re.findall('[a-zA-Z0-9]{7}', sep[0])
        if not _id or _id == ' ':
            continue
        author_name = sep[1]
        msg = sep[2]
        commits.append({
            'commit_id': _id,
            'author_name': author_name,
            'commit_message': msg,
        })

    return (commits)


def compare_with_remote(repo, branch, commit_id):
    if exists(repo):
        chdir(repo)
        pull(branch)
    else:
        clone(repo, branch)
        chdir(repo)

    diff = commit_diff(commit_id)
    commits = parse_commit_diff(diff)

    return commits


def get_new_commits_after(repo, branch, commit):
    commits = []

    workspace, owd = prepare_workspace()
    chdir(workspace)

    try:
        commits = compare_with_remote(repo, branch, commit)

    except Exception as e:
        raise Exception('ERROR for {}: {}'.format(repo, repr(e)))

    finally:
        chdir(owd)

    return (commits)


def prepare_workspace():
    original_working_dir = os.path.abspath(os.curdir)
    workspace = '/var/lib/repo'

    if exists(workspace):
        pass
    else:
        os.makedirs(workspace)

    return workspace, original_working_dir
