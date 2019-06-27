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

    def get_latest_deployment_details(self, service):
        """
        gets the latest deployment details for the service
        """

        dplymts = Deployments.objects.filter(service=service).\
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

    def get_saved_status(self, service):
        """
        returns last updated status of a service
        """
        return (to_dict(Status.objects.filter(app=service)).first())

    def get_undeployed_commits(self, service, commit_hash, branch):
        """
        returns commits yet to be deployed of a particular branch
        """

        cur_st = current_status(service, branch, commit_hash)

        Status.objects.modify(
            upsert=True, set__app=cur_st.get('app'),
            set__status=cur_st.get('status'),
            set__message=cur_st.get('message'),
            set__last_update=cur_st.get('last_update')
        )

        return cur_st
