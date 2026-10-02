import Pyro5.api
from django.core.management.base import BaseCommand
from api_app.models import Buku, Anggota

# Decorator ini mengekspos class agar bisa dipanggil dari jarak jauh
@Pyro5.api.expose
class AdminPerpustakaan(object):
    def ringkasan_sistem(self):
        jml_buku = Buku.objects.count()
        jml_anggota = Anggota.objects.count()
        return f"Sistem terhubung. Total: {jml_buku} judul buku dan {jml_anggota} anggota terdaftar."

    def tambah_stok(self, isbn, jumlah):
        try:
            buku = Buku.objects.get(isbn=isbn)
            buku.stok_tersedia += jumlah
            buku.save()
            return f"Stok buku '{buku.judul}' berhasil ditambah! Stok saat ini: {buku.stok_tersedia}."
        except Buku.DoesNotExist:
            return "Gagal: Buku dengan ISBN tersebut tidak ditemukan di database."

class Command(BaseCommand):
    help = 'Menjalankan server RMI (Pyro5) untuk Desktop Admin Pustakawan'

    def handle(self, *args, **kwargs):
        # Menjalankan daemon Pyro5 di port 9090
        daemon = Pyro5.api.Daemon(host="localhost", port=9090)
        
        # Mendaftarkan class AdminPerpustakaan dengan ID "admin.perpus"
        uri = daemon.register(AdminPerpustakaan, "admin.perpus")
        
        self.stdout.write(self.style.SUCCESS('Server RMI (Pyro5) menyala di port 9090...'))
        self.stdout.write(self.style.WARNING(f'URI: {uri}'))
        
        # Memulai loop untuk mendengarkan permintaan dari PC Klien
        daemon.requestLoop()