import uvicorn
from fastapi import FastAPI
from fastapi_chameleon import global_init
from starlette.staticfiles import StaticFiles

from pypi.config import get_settings
from pypi.data import db_session
from pypi.views import accounts, home, packages

app = FastAPI()


def configure_templates():
    global_init(template_folder="pypi/templates", auto_reload=True)
    app.mount("/static", StaticFiles(directory="pypi/static"), name="static")


def configure_routes():
    app.include_router(home.router)
    app.include_router(accounts.router, prefix="/account")
    app.include_router(packages.router, prefix="/project")


def configure_db(dev_mode: bool):
    db_session.global_init(get_settings().db_url)


def configure_app():
    configure_templates()
    configure_routes()
    configure_db(dev_mode=True)


def main():
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
else:
    configure_app()
