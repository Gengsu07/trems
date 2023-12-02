from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class ppmpkm_base(SQLModel):
    admin: str = Field(index=True)
    kdmap: str = Field(index=True)
    kdbayar: str
    masa: str
    masa2: str
    tahun: str
    tanggalbayar: int
    bulanbayar: int
    tahunbayar: int
    datebayar: date = Field(index=True)
    nominal: float
    ket: str
    seksi: Optional[str] = None
    segmentasi_wp: Optional[str] = None
    jenis_wp: Optional[str] = None
    nama_klu: Optional[str] = None
    kd_kategori: Optional[str] = Field(index=True)
    nm_kategori: Optional[str] = None
    nm_golpok: Optional[str] = None
    map: str = Field(index=True)
    npwp15: str = Field(primary_key=True, index=True)
    nama_wp: str
    nama_ar: str
    ntpn: str = Field(index=True)


class ppmpkm(ppmpkm_base, table=True):
    pass
