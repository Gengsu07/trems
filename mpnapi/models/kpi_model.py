from sqlmodel import SQLModel


class Bruto(SQLModel):
    bruto_cy: int
    bruto_py: int
    selisih_bruto: int
    persen_naik: float


class Netto(SQLModel):
    netto_cy: int
    netto_py: int
    selisih_netto: int
    persen_naik: float
