from common.utils.externals import to_dict

from models import Deployments, Status
from services.run import current_status
from errors import ServiceException


class DeploymentService(object):

    def get_environment_deployments(self, env):
        """
        returns docs belonging to environment: 'env'
        """

        return Deployments.objects.filter(environment=env)

    def get_latest_deployment_details(self, service, env='testing'):
        """
        gets the latest deployment details for the service
        """

        dplymts = Deployments.objects.filter(service=service,
                                             environment=env).\
            order_by('-deployed_date').first()

        if not dplymts:
            raise ServiceException('no deployment for given service')

        return to_dict(dplymts)

    def get_distinct_app_names(self, environment='testing'):
        """
        returns list of distinct services under specific environment
        """

        env = self.get_environment_deployments(environment)

        return env.distinct('service')

    def get_saved_status(self, env='testing'):
        """
        returns last updated status for services
        """

        apps = self.get_distinct_app_names(env)

        statuses = Status.objects.filter(app__in=apps, environment=env)

        statuses = filter(lambda x: x.status != '[UNKNOWN]', statuses)

        updated_sts = {
            status.app: to_dict(status) for status in statuses
        }

        return_out = {}

        for app, status in updated_sts.items():
            details = self.get_latest_deployment_details(app, env)
            status.update({'current_branch': details.get('branch')})

            return_out.update({app: status})

        return return_out

    def get_undeployed_commits(self, service, commit_hash, branch):
        """
        returns commits yet to be deployed of a particular branch
        """

        cur_st = current_status(service, branch, commit_hash)

        return cur_st

    def store_status_for_the_date(self, env='testing'):
        """
        stores the current status of the app for todays date
        """

        apps = self.get_distinct_app_names(env)

        ltst_dplymnts = {
            app: self.get_latest_deployment_details(app, env) for app in apps
        }

        current_status = {
            app: self.get_undeployed_commits(
                app, dplymt.get('commit_hash'), dplymt.get('branch')
            ) for app, dplymt in ltst_dplymnts.items()
        }

        for svc, status in current_status.items():
            Status.objects.filter(app=svc, environment=env).modify(
                upsert=True, set__messages=status.get('message'),
                set__app=svc, set__environment=env,
                set__status=status.get('status'),
                set__last_update=status.get('last_update'),
            )
