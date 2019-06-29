import click


@click.command()
def update_status():
    """
    updates the status of all the repositories
    """

    from services import DeploymentService
    from choices import ENVIRONMENT_CHOICES

    srv = DeploymentService()

    for env in ENVIRONMENT_CHOICES:
        srv.store_status_for_the_date(env)


if __name__ == '__main__':
    update_status()
