from django.db import models
from django.utils import timezone
from datetime import timedelta

class Buku(models.Model):
    judul = models.CharField(max_length=255)
    penulis = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    stok_tersedia = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['judul'], name='idx_judul_btree'),
            models.Index(fields=['penulis'], name='idx_penulis_btree'),
        ]

    def __str__(self):
        return self.judul

class Anggota(models.Model):
    nim = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=255)
    status_aktif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nim} - {self.nama}"

def tenggat_default():
    return timezone.now() + timedelta(days=7)

class TransaksiPeminjaman(models.Model):
    STATUS_CHOICES = [
        ('DIPINJAM', 'Dipinjam'),
        ('DIKEMBALIKAN', 'Dikembalikan'),
        ('TERLAMBAT', 'Terlambat'),
    ]

    buku = models.ForeignKey(Buku, on_delete=models.RESTRICT)
    anggota = models.ForeignKey(Anggota, on_delete=models.RESTRICT)
    tanggal_pinjam = models.DateTimeField(auto_now_add=True)
    tenggat_kembali = models.DateTimeField(default=tenggat_default)
    tanggal_dikembalikan = models.DateTimeField(null=True, blank=True)
    denda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DIPINJAM')

    class Meta:
        indexes = [
            models.Index(fields=['anggota', 'status'], name='idx_anggota_status'),
        ]

    def __str__(self):
        return f"{self.anggota.nama} meminjam {self.buku.judul}"