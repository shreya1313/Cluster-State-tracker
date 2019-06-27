from flask import render_template, request

from services import DeploymentService
from forms import EnvironmentChoice


srv = DeploymentService()


def deployed():
    form = EnvironmentChoice()

    if request.method == 'POST':
        d = srv.get_distinct_app_names(request.form['env_choice'])
        cur_st = [srv.get_saved_status(s) for s in d]
        return render_template(
            'deployed.html', len_app=len(d), dep=d, form=form, cur_st=cur_st)
    else:
        d = srv.get_distinct_app_names()
        cur_st = [srv.get_saved_status(s) for s in d]
        return render_template(
            'deployed.html', len_app=len(d), dep=d, form=form, cur_st=cur_st)


def details(service):
    details = srv.get_latest_deployment_details(service)

    commits = srv.get_undeployed_commits(
        service, details.get('commit_hash'), details.get('branch'))

    return render_template(
        'details.html',
        cur_branch=details.get('branch'), commits=commits
    )
