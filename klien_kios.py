import sys
import os
import grpc

# Setup path agar klien bisa membaca file hasil compile gRPC
sys.path.append(os.path.join(os.path.dirname(__file__), 'api_app', 'rpc'))

import peminjaman_pb2
import peminjaman_pb2_grpc

def jalankan_kios():
    # Membuka koneksi (channel) ke server gRPC di port 50051
    print("Membuka koneksi ke Server gRPC...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = peminjaman_pb2_grpc.PeminjamanServiceStub(channel)
        
        print("\n--- KIOS SELF-CHECKOUT PERPUSTAKAAN ---")
        nim_input = input("Scan KTM (Masukkan NIM): ")
        isbn_input = input("Scan Buku (Masukkan ISBN): ")
        
        print("\nMengirim data ke server (milidetik)...")
        
        # Membuat paket data Request
        request = peminjaman_pb2.CheckoutRequest(nim=nim_input, isbn=isbn_input)
        
        try:
            # Memanggil fungsi CheckoutBuku di server secara remote (RPC)
            response = stub.CheckoutBuku(request)
            
            print("\n=== RESPON DARI SERVER ===")
            if response.sukses:
                print(f"✅ {response.pesan}")
            else:
                print(f"❌ {response.pesan}")
            print("==========================\n")
        except grpc.RpcError as e:
            print(f"❌ Gagal terhubung ke server: {e.details()}")

if __name__ == '__main__':
    jalankan_kios()