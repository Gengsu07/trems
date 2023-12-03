from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, and_, case, func, select

from ..database.db import get_db
from ..filter.base_filter import filter_base
from ..models.persektor import persektor
from ..models.ppmpkm import ppmpkm

router = APIRouter()


@router.get("/sektor_bruto", status_code=200, response_model=List[persektor])
def get_persektor_bruto(
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

    stmt = (
        select(
            ppmpkm.kd_kategori,
            ppmpkm.nm_kategori,
            func.sum(case((ppmpkm.tahunbayar == tgl_awal.year, ppmpkm.nominal))).label(
                "bruto_cy"
            ),
            func.sum(
                case((ppmpkm.tahunbayar == tgl_awal.year - 1, ppmpkm.nominal))
            ).label("bruto_py"),
        )
        .where(base_stmt)
        .group_by(ppmpkm.kd_kategori, ppmpkm.nm_kategori)
    )
    data = session.exec(stmt).all()
    if all(x is None for row in data for x in row):
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    return data


@router.get("/sektor_netto", status_code=200, response_model=List[persektor])
def get_persektor_netto(
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

    stmt = (
        select(
            ppmpkm.kd_kategori,
            ppmpkm.nm_kategori,
            func.sum(case((ppmpkm.tahunbayar == tgl_awal.year, ppmpkm.nominal))).label(
                "bruto_cy"
            ),
            func.sum(
                case((ppmpkm.tahunbayar == tgl_awal.year - 1, ppmpkm.nominal))
            ).label("bruto_py"),
        )
        .where(base_stmt)
        .group_by(ppmpkm.kd_kategori, ppmpkm.nm_kategori)
    )
    data = session.exec(stmt).all()
    if all(x is None for row in data for x in row):
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    return data
