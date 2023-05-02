import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import db

origins = ["http://localhost:3000"]  # frontend


def init_app():
    db.init()

    app = FastAPI(
        title="CRUD List",
        description="sort and filter through paginated list",
        version="0.1"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    from controllers import person

    app.include_router(person.router)

    return app


app = init_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)
