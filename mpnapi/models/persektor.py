from typing import Optional

from sqlmodel import SQLModel


class persektor(SQLModel):
    kd_kategori: Optional[str]
    nm_kategori: Optional[str]
    bruto_cy: Optional[float]
    bruto_py: Optional[float]
