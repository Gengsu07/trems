from dateutil.relativedelta import relativedelta
from sqlmodel import and_, or_

from ..models.ppmpkm import ppmpkm


# kita bikin base condition dlu, yaitu filter by date awal tahun sampai sekarang dan tahun yg lalu waktu yg sama
def filter_base(tgl_awal, tgl_akhir, kdmap, sektor, npwp15, nama_wp):
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
    return base_stmt
