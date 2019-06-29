from celerybeatmongo.models import PeriodicTask


SCHEDULES = [
    {
        'name': 'update-repo-status',
        'task': 'tasks.save_repo_status',
        'crontab': PeriodicTask.Crontab(**{
            'minute': '*/120',
        }),
        'enabled': True
    },
]
