from apistar import Route, App
from app.api.routes import welcome, extract

routes = [
    Route('/', 'GET', welcome),
    Route('/translate', 'POST', extract)
]


def application_factory(settings=None, routes=routes):
    """Returns an instance of Cookie API"""
    if settings is None:
        settings = {}

    return App(routes=routes)
