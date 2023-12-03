from fastapi import FastAPI

from mpnapi.database.db import create_db_and_tables
from mpnapi.routers.kpi_api import router as mpn_router
from mpnapi.routers.sektor_api import router as sektor_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(mpn_router, tags=["KPI"])
app.include_router(sektor_router, tags=["Per Sektor"])
