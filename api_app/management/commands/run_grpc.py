import sys
import os
import grpc
from concurrent import futures
from django.core.management.base import BaseCommand
from django.conf import settings

# --- TAMBAHKAN MODUL INI UNTUK MUTUAL EXCLUSION ---
from django.db import transaction

sys.path.append(os.path.join(settings.BASE_DIR, 'api_app', 'rpc'))

from api_app.models import Buku, Anggota, TransaksiPeminjaman
import peminjaman_pb2
import peminjaman_pb2_grpc

class PeminjamanServicer(peminjaman_pb2_grpc.PeminjamanServiceServicer):
    def CheckoutBuku(self, request, context):
        try:
            # PENERAPAN MUTUAL EXCLUSION (CENTRALIZED ALGORITHM)
            # atomic() memastikan proses ini tidak bisa diganggu gugat hingga selesai
            with transaction.atomic():
                
                # select_for_update() bertindak sebagai Coordinator yang 
                # mengunci (Grant) baris data ini. Jika ada Kios lain yang 
                # mencoba mengakses, mereka akan dimasukkan ke antrean (Queue).
                buku = Buku.objects.select_for_update().get(isbn=request.isbn)
                anggota = Anggota.objects.get(nim=request.nim)

                if buku.stok_tersedia > 0:
                    buku.stok_tersedia -= 1
                    buku.save() # Setelah di-save, kunci (akses) dilepas (Release)

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