# LokerLens

LokerLens adalah prototype website full-stack untuk membantu mahasiswa, fresh graduate, dan freelancer pemula mengecek indikasi risiko lowongan digital sebelum apply.

## Tujuan Project

Project ini dibuat untuk:

- Membantu pengguna membaca transparansi dan potensi risiko sebuah lowongan.
- Mengubah teks lowongan menjadi hasil analisis yang mudah dipahami.
- Menyediakan fitur awal seperti Trust Score, Missing Information Checker, Red Flag Detector, Personal Data Warning, Safe Apply Checklist, dan Recruiter Question Generator.
- Mendukung tugas Analisis Kelayakan Bisnis dengan data, insight, dan validasi masalah dari pola lowongan digital nyata.

## Hubungan Data Dengan LokerLens

Modul data LokerLens mengumpulkan lowongan dari sumber publik yang aman diakses. Data scraping digunakan untuk menemukan pola risiko lowongan digital, misalnya informasi perusahaan yang tidak jelas, kompensasi tidak disebutkan, permintaan data pribadi, permintaan pembayaran, janji tidak realistis, dan detail kerja yang kurang transparan.

Pola tersebut menjadi dasar fitur LokerLens:

- `Trust Score`: memberi skor awal berdasarkan kelengkapan dan indikasi risiko.
- `Missing Information Checker`: mencari informasi penting yang tidak disebutkan.
- `Red Flag Detector`: mendeteksi kategori risiko dari teks lowongan.
- `Personal Data Warning`: memberi peringatan jika lowongan meminta data sensitif.
- `Safe Apply Checklist`: membantu pengguna mengecek langkah aman sebelum apply.
- `Recruiter Question Generator`: menyusun pertanyaan klarifikasi untuk recruiter.

Untuk tugas Analisis Kelayakan Bisnis, dataset dan insight EDA dipakai untuk menunjukkan bahwa masalah lowongan digital berisiko memang dapat diamati dari data real. Hasil ini membantu menjelaskan kebutuhan pengguna, value proposition, risiko operasional, dan dasar fitur produk pada Business Model Canvas.

## Struktur Folder

```text
backend/          Backend FastAPI, database, auth, dan endpoint scanner
frontend/         Frontend React Vite untuk UI LokerLens
ml/               Eksperimen baseline ML internal
lokerlens-data/   Scraper, cleaning, labeling, notebook EDA, figures, reports
```

## Sumber Data

Daftar sumber berada di `lokerlens-data/data/raw/source_urls.txt`. Sumber dapat berupa:

- Public JSON API: Arbeitnow, Remotive, The Muse, Remote OK.
- Public HTML job listing pages: Dealls, Jobstreet Indonesia, LinkedIn public pages, dan sumber lain yang bisa diakses tanpa login.

Jika sebuah URL gagal, timeout, diblokir, membutuhkan login, captcha, paywall, atau struktur HTML tidak bisa diparse, proses tidak dibypass. Error disimpan di `lokerlens-data/data/raw/scraping_errors.csv` dan proses lanjut ke URL berikutnya.

Dataset utama tidak menggunakan dummy, synthetic, atau fake job posting.

## Menjalankan Modul Data

Masuk ke folder data module:

```powershell
cd C:\Users\firma\Documents\Python\Kuliah\AKB\LokerLens\lokerlens-data
pip install -r requirements.txt
```

Jika `data/raw/scraped_job_posts.csv` sudah ada dan berisi data real, jangan jalankan scraping ulang agar dataset tidak tertimpa. Jalankan scraping hanya jika raw dataset belum ada atau memang ingin refresh data publik:

```powershell
python scraping\scraper_public_jobs.py
```

Jalankan cleaning dan labeling:

```powershell
python scraping\clean_and_label_data.py
```

Jalankan notebook visualisasi:

```powershell
python -m nbconvert --to notebook --execute --inplace notebooks\01_lokerlens_eda_and_visualization.ipynb --ExecutePreprocessor.timeout=180
```

## Output Modul Data

- `lokerlens-data/data/raw/scraped_job_posts.csv`
- `lokerlens-data/data/raw/scraping_errors.csv`
- `lokerlens-data/data/raw/raw_collection_log.csv`
- `lokerlens-data/data/processed/lokerlens_dataset_clean.csv`
- `lokerlens-data/data/processed/lokerlens_dataset_labeled.csv`
- `lokerlens-data/data/processed/red_flag_summary.csv`
- `lokerlens-data/figures/*.png`
- `lokerlens-data/reports/insight_summary.md`
- `lokerlens-data/reports/data_dictionary.md`

## Menjalankan Website

Backend:

```powershell
cd C:\Users\firma\Documents\Python\Kuliah\AKB\LokerLens\backend
copy .env.example .env
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:

```powershell
cd C:\Users\firma\Documents\Python\Kuliah\AKB\LokerLens\frontend
npm install
$env:VITE_API_BASE_URL="http://127.0.0.1:8000"
npm run dev -- --port 5173
```

Buka `http://127.0.0.1:5173`.

## Etika Scraping

Scraper hanya mengambil data dari sumber publik yang aman diakses. Project ini tidak melakukan login otomatis, tidak melewati captcha, tidak melewati paywall, dan tidak melakukan bypass keamanan. Informasi sensitif seperti email personal, nomor telepon, OTP, password, nomor rekening, atau nomor identitas tidak disimpan mentah dan dinormalisasi menjadi label kategori.

## Keterbatasan Data

Jumlah data bergantung pada ketersediaan sumber publik saat script dijalankan. Beberapa situs dapat membatasi request, mengubah struktur HTML, atau menolak akses otomatis. Label risiko dan trust score bersifat rule-based sehingga hasilnya digunakan sebagai indikasi awal, bukan keputusan mutlak bahwa sebuah lowongan aman atau berbahaya.

## Catatan Security

- Password aplikasi disimpan sebagai hash bcrypt.
- JWT memiliki expiration sesuai konfigurasi backend.
- Untuk prototype, access token disimpan di localStorage.
- Untuk production, gunakan httpOnly secure cookie, HTTPS, rate limiting, dan rotasi secret.
