from fastapi import FastAPI

from mpnapi.database.db import create_db_and_tables
from mpnapi.routers.kpi_api import router as mpnrouter

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(mpnrouter)
