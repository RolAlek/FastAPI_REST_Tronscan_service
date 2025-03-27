from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="FasAPI Tron Scanner", docs_url="/api/docs")
    return app
