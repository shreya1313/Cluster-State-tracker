import mongoengine as me


class Deployments(me.Document):

    service = me.StringField(required=True)
    environment = me.StringField(required=True)
    image_uri = me.StringField(required=True)
    commit_hash = me.StringField(required=True)
    commit_message = me.StringField(required=True)
    deployed_date = me.DateTimeField()
    branch = me.StringField(required=True)


class Status(me.Document):

    environment = me.StringField(required=True)
    app = me.StringField(required=True)
    status = me.StringField(required=True)
    messages = me.ListField(required=True)
    last_update = me.StringField(required=True)

    meta = {
        'indexes': [
            ('environment', 'app', ),
        ],
        'auto_create_index': True,
        'index_background': True
    }
