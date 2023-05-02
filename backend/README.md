## FastAPI CRUD app

* pagination
* sorting
* filtering

pip packages: fastapi, uvicorn, sqlmodel, pydantic, sqlalchemy, asyncpg, alembic


#### Run Commands

```bash
    cd app/
    alembic init migrations
    alembic revision --autogenerate -m
    alembic upgrade head
```
