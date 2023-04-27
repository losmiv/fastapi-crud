import uvicorn
from fastapi import FastAPI
from config import db


def init_app():
    db.init()

    app = FastAPI(
        title="CRUD List",
        description="sort, paginate, filter list",
        version="0.1"
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    return app


app = init_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)
