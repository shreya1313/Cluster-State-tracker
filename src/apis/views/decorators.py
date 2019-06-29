from flask import request, jsonify
from flask import g
from clients.auth_client import AuthClient
from clients.utils.errors import ClientException


def extract_authorization_key():
    """
    extracts authorization keys from headers or cookies
    """

    return request.headers.get('Authorization') or \
        request.cookies.get('authorization_key')


def internal_user_required(func):

    def wrapper(*args, **kwargs):
        authorization_key = extract_authorization_key()

        try:
            output = AuthClient.login_internal_user(
                auth_key=authorization_key)
        except ClientException as exc:
            return jsonify({'errorMessage': exc.args[0]}), 401

        if not output.get('is_active'):
            return jsonify({
                "errorMessage": "User is inactive"
            }), 401

        setattr(g, 'user', output)

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__

    return wrapper
