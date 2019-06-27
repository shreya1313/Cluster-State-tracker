def test_scaffolding_setup(client):
    response = client.get('/')

    assert response.data.decode('utf-8') == \
        "Welcome to the {} application".format(
            client.application.config.get('APPLICATION_NAME'))
