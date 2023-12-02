from typing import List

from fastapi import Depends, FastAPI, Query
from sqlmodel import Session, select

from mpnapi.database.db import create_db_and_tables, get_db
from mpnapi.models.ppmpkm import ppmpkm, ppmpkm_base

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", response_model=List[ppmpkm_base])
def get_ppmpkm(
    *,
    session: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    data = session.exec(select(ppmpkm).offset(offset).limit(limit)).all()
    return data
