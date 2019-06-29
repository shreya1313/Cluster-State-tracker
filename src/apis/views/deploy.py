from flask import render_template, request

from services import DeploymentService
from forms import EnvironmentChoice
from .decorators import internal_user_required


srv = DeploymentService()


@internal_user_required
def deployed():
    form = EnvironmentChoice()

    if request.method == 'POST':
        cur_st = srv.get_saved_status(request.form['env_choice'])

        return render_template('deployed.html', form=form, cur_st=cur_st)
    else:
        cur_st = srv.get_saved_status()

        return render_template('deployed.html', form=form, cur_st=cur_st)


@internal_user_required
def details(service):
    env = request.args.to_dict().get('env')

    cur_st = srv.get_saved_status(env)

    details = srv.get_latest_deployment_details(service, env)

    status = cur_st.get(service)

    return render_template(
        'details.html',
        cur_branch=details.get('branch'), commits=status)
