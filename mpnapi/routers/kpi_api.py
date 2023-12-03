from datetime import date
from typing import List, Optional

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, and_, case, func, select

from ..database.db import get_db
from ..filter.base_filter import filter_base
from ..models.kpi_model import Bruto, Netto
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


@router.get("/bruto", status_code=200, response_model=Bruto)
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
    base_stmt = filter_base(tgl_awal, tgl_akhir, kdmap, sektor, npwp15, nama_wp)

    base_stmt = and_(base_stmt, ppmpkm.ket.in_(["MPN", "SPM"]))

    stmt = select(
        func.sum(case((ppmpkm.tahunbayar == tgl_awal.year, ppmpkm.nominal))).label(
            "bruto_cy"
        ),
        func.sum(case((ppmpkm.tahunbayar == tgl_awal.year - 1, ppmpkm.nominal))).label(
            "bruto_py"
        ),
    ).where(base_stmt)

    data = session.exec(stmt).first()
    if all(x is None for x in data):
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    results = {
        "bruto_cy": int(data.bruto_cy),
        "bruto_py": int(data.bruto_py),
        "selisih_bruto": int(data.bruto_cy - data.bruto_py),
        "persen_naik": round(
            ((data.bruto_cy - data.bruto_py) / data.bruto_py) * 100, 2
        ),
    }

    return results


@router.get("/netto", status_code=200, response_model=Netto)
def get_netto(
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
    base_stmt = filter_base(tgl_awal, tgl_akhir, kdmap, sektor, npwp15, nama_wp)

    stmt = select(
        func.sum(case((ppmpkm.tahunbayar == tgl_awal.year, ppmpkm.nominal))).label(
            "netto_cy"
        ),
        func.sum(case((ppmpkm.tahunbayar == tgl_awal.year - 1, ppmpkm.nominal))).label(
            "netto_py"
        ),
    ).where(base_stmt)

    data = session.exec(stmt).first()
    if all(x is None for x in data):
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    netto_cy = data.netto_cy
    netto_py = data.netto_py
    results = {
        "netto_cy": int(netto_cy),
        "netto_py": int(netto_py),
        "selisih_netto": int(netto_cy - netto_py),
        "persen_naik": round(((netto_cy - netto_py) / netto_py) * 100, 2),
    }

    return results
