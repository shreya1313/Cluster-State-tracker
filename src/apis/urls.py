from .views import deploy


api_urls = [
    ('/deployed', deploy.deployed, ['GET', 'POST'], 'get all the unique services per page'),
    ('/details/<service>', deploy.details, ['GET'], 'get details for each unique app'),    
]
