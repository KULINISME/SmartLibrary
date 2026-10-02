import Pyro5.api

# Terhubung ke server RMI menggunakan URI (Host dan Port) yang kita set di server
URI = "PYRO:admin.perpus@localhost:9090"
admin_perpus = Pyro5.api.Proxy(URI)

def jalankan_desktop_admin():
    print("=== APLIKASI DESKTOP PUSTAKAWAN ===")
    print("1. Cek Ringkasan Sistem")
    print("2. Tambah Stok Buku Baru (Restock)")
    
    pilihan = input("Pilih menu (1/2): ")
    
    print("\nMemproses via RMI...")
    try:
        if pilihan == '1':
            # Memanggil fungsi di server secara langsung
            hasil = admin_perpus.ringkasan_sistem()
            print(f"Server menjawab: {hasil}")
        
        elif pilihan == '2':
            isbn = input("Masukkan ISBN Buku: ")
            jml = int(input("Berapa buku yang baru datang? "))
            
            # Memanggil fungsi di server secara langsung
            hasil = admin_perpus.tambah_stok(isbn, jml)
            print(f"Server menjawab: {hasil}")
        else:
            print("Pilihan tidak valid.")
            
    except Exception as e:
        print(f"Gagal terhubung ke Server RMI: {e}")

if __name__ == '__main__':
    jalankan_desktop_admin()