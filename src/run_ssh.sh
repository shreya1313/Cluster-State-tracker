#!/bin/sh

set -x

eval "$(ssh-agent -s)"

echo -e "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

set +x

# command coming after the execution of shell script
"$@"
