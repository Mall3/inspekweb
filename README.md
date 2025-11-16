# 🕸️ InspekWeb: Advanced Web Visitor & Fingerprint Spoofer

InspekWeb adalah skrip Python asinkron yang memanfaatkan Playwright untuk melakukan kunjungan web dengan simulasi perilaku manusia dan teknik *spoofing* *browser fingerprint* tingkat lanjut. Skrip ini dirancang untuk berjalan di lingkungan server (*headless*) tanpa X Server.

---

## ⚙️ Persyaratan Sistem

Skrip ini dioptimalkan untuk berjalan pada VPS/Server Linux (Ubuntu/Debian) yang fresh.

### 1. Instalasi Dependensi Dasar VPS (Fresh Install)

Jika kamu menggunakan VPS/server Linux yang *fresh* (baru), kamu perlu menginstal beberapa *library* dasar yang dibutuhkan Playwright untuk menjalankan Chromium.

Jalankan perintah berikut di terminal kamu:

```bash
# Update sistem
sudo apt update
sudo apt upgrade -y

# Instal dependensi Playwright (Chromium dependencies)
sudo apt install -y build-essential libnss3 libatk-bridge2.0-0 libcups2 libdrm-dev libxkbcommon-dev libgbm-dev

2. Instalasi Python dan Lingkungan Virtual
Pastikan kamu memiliki Python 3 (disarankan Python 3.8 ke atas) dan Virtual Environment (venv) yang terinstal:

# Instal Python dan venv (jika belum ada)
sudo apt install -y python3 python3-pip python3-venv


🚀 Panduan Instalasi & Persiapan
Ikuti langkah-langkah ini untuk menyiapkan lingkungan kerja:
Langkah 1: Buat dan Aktifkan Lingkungan Virtual (venv)
Membuat virtual environment sangat penting untuk menghindari konflik dependensi.

# Buat direktori project dan masuk ke dalamnya
mkdir inspekweb
cd inspekweb

# Buat lingkungan virtual
python3 -m venv venv

# Aktifkan lingkungan virtual
source venv/bin/activate

# Kamu akan melihat (venv) di depan prompt kamu.

Langkah 2: Instal Playwright dan Dependensi Python
Setelah venv aktif, instal Playwright dan unduh biner browser Chromium:

# Instal Playwright
pip install playwright

# Instal biner browser Chromium (ini WAJIB)
playwright install chromium

Langkah 3: Tambahkan Kode Skrip
Buat file bernama inspekweb.py di dalam direktori inspekweb.
Salin dan tempel kode lengkap InspekWeb V5 ke dalam file tersebut.
💡 Konfigurasi Penting (Fake IP)
Jika kamu ingin menggunakan fitur Fake IP (Proxy), edit list proxies di bagian atas file inspekweb.py:

# Di file inspekweb.py
proxies = [
    "http://user1:pass1@ip1:port1",
    "http://user2:pass2@ip2:port2",
    "http://user3:pass3@ip3:port3",
    # ... tambahkan sisa proxy kamu di sini (misalnya, hingga 30)
]

⌨️ Cara Menjalankan Skrip
Setelah semua langkah di atas selesai, jalankan skrip dari dalam lingkungan virtual (venv harus aktif):
Format Perintah

python3 inspekweb.py <URL_TARGET> <JUMLAH_VISIT> <DELAY_PER_VISIT>

Parameter Deskripsi Contoh
URL_TARGET URL lengkap yang akan dikunjungi. https://google.com
JUMLAH_VISIT Total kunjungan yang akan dilakukan (Integer). 50
DELAY_PER_VISIT Jeda waktu (detik) antara satu kunjungan dan kunjungan berikutnya (Float). 5.5

Contoh Eksekusi
Kunjungi URL 5 kali dengan jeda 1.5 detik di antara setiap kunjungan:
(venv) root@server:~/inspekweb# python3 inspekweb.py [https://mall3.github.io/test-phising](https://mall3.github.io/test-phising) 5 1.5

Hasil Output
Hasil fingerprint dan log kunjungan akan disimpan dalam file results.json di direktori yang sama.

---

Dokumentasi ini mencakup semua langkah yang dibutuhkan mulai dari VPS kosong hingga menjalankan *script* dengan *spoofing* tingkat lanjut!

Apakah kamu ingin saya buatkan *script* *shell* kecil untuk mengotomatisasi Langkah 1 dan 2 agar instalasi di VPS baru lebih cepat?
