from __future__ import absolute_import, print_function
from datetime import datetime
from pytz import timezone

from services.repo import get_new_commits_after


def current_status(app, branch, commit):
    msg = []
    status = 'UNKNOWN'

    try:
        commits = get_new_commits_after(app, branch, commit)

        if not commits:
            status = 'OK'
        else:
            status = 'BEHIND'

            for data in commits:
                msg.append({
                    'commit_id': data.get('commit_id'),
                    'commit_message': data.get('commit_message')
                })

    except Exception as e:
        msg = e.args[0]

    # Current time in UTC
    now_utc = datetime.now(timezone('UTC'))
    # Convert to Asia/Kolkata time zone
    now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
    now_str = now_asia.strftime("%d/%m/%Y at %H:%M:%S")

    return {
        'app': app,
        'branch': branch,
        'commit': commit,
        'message': msg,
        'status': '[{}]'.format(status),
        'last_update': now_str
    }
