from datetime import date
from typing import List

import pandas as pd
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, case, func, or_, select

from ..database.db import get_db
from ..models.ppmpkm import ppmpkm, ppmpkm_base

router = APIRouter()


@router.get("/", response_model=List[ppmpkm_base])
def get_ppmpkm(
    *,
    session: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    data = session.exec(select(ppmpkm).offset(offset).limit(limit)).all()
    data_dicts = [item.to_dict() for item in data]
    df = pd.DataFrame(data_dicts)
    df = df[df["admin"] == "007"].copy()
    return df.to_dict(orient="records")


@router.get("/bruto")
def get_bruto(
    tgl_awal: date = Query(
        date(date.today().year, 1, 1),
        description="Tanggal awal, default 1 Januari tahun sekarang",
    ),
    tgl_akhir: date = Query(
        date.today(), description="Tanggal akhir, default hari ini"
    ),
    session: Session = Depends(get_db),
):
    stmt = select(
        func.sum(case((ppmpkm.tahunbayar == tgl_awal.year, ppmpkm.nominal))).label(
            "Bruto_CY"
        ),
        func.sum(case((ppmpkm.tahunbayar == tgl_awal.year - 1, ppmpkm.nominal))).label(
            "Bruto_PY"
        ),
    ).where(
        or_(
            ppmpkm.datebayar.between(tgl_awal, tgl_akhir),
            ppmpkm.datebayar.between(
                tgl_awal - relativedelta(years=1), tgl_akhir - relativedelta(years=1)
            ),
        )
    )

    data = session.exec(stmt).all()
    results = [
        {"Bruto_CY": Bruto_CY, "Bruto_PY": Bruto_PY} for Bruto_CY, Bruto_PY in data
    ]
    return results
