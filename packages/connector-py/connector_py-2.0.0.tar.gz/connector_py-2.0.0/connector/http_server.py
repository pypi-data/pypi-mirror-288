from connector.helpers import collect_methods


def collect_routes(obj: object):
    """
    Collect all methods from an object and create a route for each.
    """
    from fastapi import APIRouter

    router = APIRouter()
    commands = collect_methods(obj)
    for method in commands:
        router.add_api_route(f"/{method.__name__.replace('_', '-')}", method, methods=["POST"])
    return router


def runserver(router, port: int):
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(router)

    uvicorn.run(app, port=port)
