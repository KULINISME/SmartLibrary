import Pyro5.api

# Menggunakan 127.0.0.1 untuk tes di laptop yang sama
URI = "PYRO:admin.perpus@127.0.0.1:9090"
admin_perpus = Pyro5.api.Proxy(URI)

def jalankan_desktop_admin():
    while True:
        print("\n" + "="*35)
        print("=== APLIKASI DESKTOP PUSTAKAWAN ===")
        print("="*35)
        print("1. Cek Ringkasan Sistem")
        print("2. Lihat Daftar Buku & Stok")
        print("3. Tambah Stok Buku Baru (Restock)")
        print("4. Keluar")
        
        pilihan = input("\nPilih menu (1/2/3/4): ")
        
        if pilihan == '4':
            print("Menutup aplikasi desktop...")
            break
            
        print("\nMemproses via RMI...\n")
        try:
            if pilihan == '1':
                hasil = admin_perpus.ringkasan_sistem()
                print(f"Server menjawab: {hasil}")
            
            elif pilihan == '2':
                hasil = admin_perpus.lihat_daftar_buku()
                print(hasil)
                
            elif pilihan == '3':
                isbn = input("Masukkan ISBN Buku: ")
                jml = int(input("Berapa buku yang baru datang? "))
                hasil = admin_perpus.tambah_stok(isbn, jml)
                print(f"Server menjawab: {hasil}")
                
            else:
                print("Pilihan tidak valid.")
                
        except Exception as e:
            print(f"Gagal terhubung ke Server RMI: {e}")

if __name__ == '__main__':
    jalankan_desktop_admin()