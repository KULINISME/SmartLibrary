# Tutorial Menjalankan Proyek Smart Library (Multi-Device)

Tutorial ini akan memandu Anda untuk menjalankan arsitektur Sistem Terdistribusi yang terdiri dari **REST API**, **gRPC**, dan **RMI** dalam satu jaringan lokal (WiFi/Hotspot yang sama).

---

## Persiapan Awal: Mengetahui IP Server

Langkah ini **wajib** dilakukan di **Laptop Utama (Server)** sebelum klien lain bisa terhubung.

1. Sambungkan Laptop Utama ke jaringan WiFi.
2. Buka **Command Prompt (CMD)**, ketik `ipconfig`, lalu tekan Enter.
3. Cari baris **IPv4 Address**. Catat alamat IP tersebut (misal: `192.168.100.5`).

> **Catatan:** Seluruh IP `192.168.100.5` di tutorial ini harus diganti dengan IP Laptop Utama Anda.

---

## TAHAP 1: Menyalakan Mesin Utama (Di Laptop Server)

Di Laptop Utama, buka **3 jendela CMD** yang berbeda. Di setiap jendela, masuk ke folder proyek (`cd sister`) dan aktifkan virtual environment (`venv\Scripts\activate`).

### Terminal 1: Menyalakan Web Server (REST API)

Jalankan perintah ini agar server terbuka untuk jaringan publik:

```bat
python manage.py runserver 0.0.0.0:8000
```

Tunggu hingga muncul tulisan `Starting development server...`

### Terminal 2: Menyalakan Server Kios (gRPC)

```bat
python manage.py run_grpc
```

Tunggu hingga muncul tulisan `Server gRPC Smart Library menyala di port 50051...`

### Terminal 3: Menyalakan Server Pustakawan (RMI/Pyro5)

```bat
python manage.py run_rmi
```

Tunggu hingga muncul tulisan `Server RMI (Pyro5) menyala di port 9090...`

---

## TAHAP 2: Simulasi Klien (Di Perangkat Lain)

Pastikan perangkat klien (HP atau Laptop lain) terhubung ke jaringan WiFi yang **persis sama** dengan Laptop Utama.

### Skenario A: Mahasiswa Mencari Buku (via HP/Browser)

1. Ambil HP Anda.
2. Buka browser (Chrome/Safari).
3. Ketik alamat IP Server ditambah port `8000` dan path API. Contoh:

```
   http://192.168.100.5:8000/api/buku/
```

4. Tampilan katalog buku perpustakaan akan langsung muncul di layar HP Anda.

### Skenario B: Mesin Kios Self-Checkout (via Laptop Teman/Terminal)

Ini menyimulasikan mesin scanner **gRPC**.

1. Bawa file `klien_kios.py` dan folder `rpc` ke laptop/komputer lain.
2. Edit file `klien_kios.py`, pastikan IP-nya mengarah ke server:

```python
   with grpc.insecure_channel('192.168.100.5:50051') as channel:
```

3. Buka CMD di laptop tersebut, instal modul gRPC:

```bat
   pip install grpcio grpcio-tools
```

4. Jalankan klien:

```bat
   python klien_kios.py
```

5. Masukkan **NIM** dan **ISBN** yang terdaftar untuk melihat respons transaksinya.

### Skenario C: PC Pustakawan (via Laptop Teman/Terminal)

Ini menyimulasikan aplikasi desktop **RMI** untuk staf perpustakaan.

1. Bawa file `klien_admin.py` ke laptop lain.
2. Edit file `klien_admin.py`, pastikan alamat URI-nya mengarah ke server:

```python
   URI = "PYRO:admin.perpus@192.168.100.5:9090"
```

3. Buka CMD di laptop tersebut, instal modul Pyro5:

```bat
   pip install Pyro5
```

4. Jalankan klien:

```bat
   python klien_admin.py
```

5. Pilih menu **"2" (Tambah Stok)** untuk menambah jumlah buku secara remote, lalu verifikasi perubahannya di database server utama.
