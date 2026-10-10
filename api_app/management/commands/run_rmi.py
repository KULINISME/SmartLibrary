import Pyro5.api
from django.core.management.base import BaseCommand
from django.db import transaction
from api_app.models import Buku, Anggota

@Pyro5.api.expose
class AdminPerpustakaan(object):
    def ringkasan_sistem(self):
        jml_buku = Buku.objects.count()
        jml_anggota = Anggota.objects.count()
        return f"Sistem terhubung. Total: {jml_buku} judul buku dan {jml_anggota} anggota terdaftar."

    # FITUR BARU: MELIHAT DAFTAR BUKU
    def lihat_daftar_buku(self):
        buku_list = Buku.objects.all()
        if not buku_list:
            return "Belum ada data buku di database."
        
        # Merapikan tampilan data ke dalam format tabel teks
        hasil = "=== DAFTAR BUKU PERPUSTAKAAN ===\n"
        hasil += f"{'ISBN':<15} | {'JUDUL':<35} | {'STOK'}\n"
        hasil += "-" * 65 + "\n"
        for b in buku_list:
            # Memotong judul jika terlalu panjang agar tabel tetap rapi
            hasil += f"{b.isbn:<15} | {b.judul[:33]:<35} | {b.stok_tersedia}\n"
        
        return hasil

    def tambah_stok(self, isbn, jumlah):
        try:
            # PENERAPAN MUTUAL EXCLUSION
            with transaction.atomic():
                buku = Buku.objects.select_for_update().get(isbn=isbn)
                buku.stok_tersedia += jumlah
                buku.save()
                return f"Stok buku '{buku.judul}' berhasil ditambah! Stok saat ini: {buku.stok_tersedia}."
        except Buku.DoesNotExist:
            return "Gagal: Buku dengan ISBN tersebut tidak ditemukan di database."
        except Exception as e:
            return f"Terjadi kesalahan sistem: {str(e)}"


class Command(BaseCommand):
    help = 'Menjalankan server RMI (Pyro5) untuk Desktop Admin Pustakawan'

    def handle(self, *args, **kwargs):
        # Menggunakan 0.0.0.0 agar bisa diakses dari jaringan luar
        daemon = Pyro5.api.Daemon(host="0.0.0.0", port=9090)
        uri = daemon.register(AdminPerpustakaan, "admin.perpus")
        
        self.stdout.write(self.style.SUCCESS('Server RMI (Pyro5) menyala di port 9090 (Safe Mode: Mutual Exclusion Aktif)...'))
        self.stdout.write(self.style.WARNING(f'URI: {uri}'))
        
        # Memulai loop untuk mendengarkan permintaan dari klien
        daemon.requestLoop()