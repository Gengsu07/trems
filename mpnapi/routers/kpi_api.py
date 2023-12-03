from datetime import date
from typing import List, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, and_, case, func, or_, select

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
    sektor: Optional[str] = None,
    kdmap: Optional[str] = None,
    npwp15: Optional[str] = None,
    nama_wp: Optional[str] = None,
    session: Session = Depends(get_db),
):
    # kita bikin base condition dlu, yaitu filter by date awal tahun sampai sekarang dan tahun yg lalu waktu yg sama
    base_stmt = or_(
        ppmpkm.datebayar.between(tgl_awal, tgl_akhir),
        ppmpkm.datebayar.between(
            tgl_awal - relativedelta(years=1), tgl_akhir - relativedelta(years=1)
        ),
    )

    # kalau ada kdmap atau sektor atau filter yg lain maka kita tambahkan kondisinya pakai and_
    if kdmap:
        base_stmt = and_(base_stmt, ppmpkm.kdmap == kdmap)
    if sektor:
        base_stmt = and_(base_stmt, ppmpkm.kd_kategori == sektor)
    if npwp15:
        base_stmt = and_(base_stmt, ppmpkm.npwp15 == npwp15)
    if nama_wp:
        base_stmt = and_(base_stmt, ppmpkm.nama_wp == nama_wp)

    stmt = select(
        func.sum(case((ppmpkm.tahunbayar == tgl_awal.year, ppmpkm.nominal))).label(
            "bruto_cy"
        ),
        func.sum(case((ppmpkm.tahunbayar == tgl_awal.year - 1, ppmpkm.nominal))).label(
            "bruto_py"
        ),
    ).where(base_stmt)

    data = session.exec(stmt).all()
    results = [
        {
            "bruto_cy": int(bruto_cy),
            "bruto_py": int(bruto_py),
            "selisih_bruto": int(bruto_cy - bruto_py),
            "%naik": round(((bruto_cy - bruto_py) / bruto_py) * 100, 2),
        }
        for bruto_cy, bruto_py in data
    ]
    return results
