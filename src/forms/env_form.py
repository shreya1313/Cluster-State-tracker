from flask_wtf import FlaskForm
from wtforms import SelectField
from choices import ENVIRONMENT_CHOICES


class EnvironmentChoice(FlaskForm):
    env_choice = SelectField(
        'env_choice', choices=[(c, c) for c in ENVIRONMENT_CHOICES])
