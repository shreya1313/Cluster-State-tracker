class ServiceException(Exception):

    status_code = 400

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
