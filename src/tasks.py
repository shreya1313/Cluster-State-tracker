from celery import shared_task


@shared_task
def test_task():
    print("Hello celery tasks are enabled")


@shared_task
def save_repo_status():
    from services import DeploymentService
    from choices import ENVIRONMENT_CHOICES

    srv = DeploymentService()

    for env in ENVIRONMENT_CHOICES:
        srv.store_status_for_the_date(env)
