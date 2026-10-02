import sys
import os
import grpc
from concurrent import futures
from django.core.management.base import BaseCommand
from django.conf import settings

# [SOLUSI ERROR] Daftarkan folder 'rpc' ke dalam jalur sistem Python 
# agar file hasil compile gRPC bisa saling menemukan satu sama lain.
sys.path.append(os.path.join(settings.BASE_DIR, 'api_app', 'rpc'))

from api_app.models import Buku, Anggota, TransaksiPeminjaman

# Sekarang kita bisa meng-import langsung nama filenya
import peminjaman_pb2
import peminjaman_pb2_grpc

class PeminjamanServicer(peminjaman_pb2_grpc.PeminjamanServiceServicer):
    def CheckoutBuku(self, request, context):
        try:
            buku = Buku.objects.get(isbn=request.isbn)
            anggota = Anggota.objects.get(nim=request.nim)

            if buku.stok_tersedia > 0:
                buku.stok_tersedia -= 1
                buku.save()

                TransaksiPeminjaman.objects.create(buku=buku, anggota=anggota)
                return peminjaman_pb2.CheckoutResponse(sukses=True, pesan=f"Sukses! Buku '{buku.judul}' berhasil dipinjam.")
            else:
                return peminjaman_pb2.CheckoutResponse(sukses=False, pesan="Gagal: Stok buku sedang habis.")
        
        except Buku.DoesNotExist:
            return peminjaman_pb2.CheckoutResponse(sukses=False, pesan="Gagal: Buku tidak ditemukan.")
        except Anggota.DoesNotExist:
            return peminjaman_pb2.CheckoutResponse(sukses=False, pesan="Gagal: NIM tidak terdaftar.")
        except Exception as e:
            return peminjaman_pb2.CheckoutResponse(sukses=False, pesan=f"Error Sistem: {str(e)}")

class Command(BaseCommand):
    help = 'Menjalankan server gRPC untuk Kios Mandiri Smart Library'

    def handle(self, *args, **kwargs):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        peminjaman_pb2_grpc.add_PeminjamanServiceServicer_to_server(PeminjamanServicer(), server)
        
        server.add_insecure_port('[::]:50051')
        self.stdout.write(self.style.SUCCESS('Server gRPC Smart Library menyala di port 50051...'))
        server.start()
        server.wait_for_termination()