# LokerLens - Data & ML Module

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
data/         Dataset mentah (raw) dan hasil pemrosesan (processed)
figures/      Visualisasi hasil analisis data/EDA
notebooks/    Jupyter Notebook untuk EDA dan visualisasi
reports/      Laporan business insight dan kamus data
scraping/     Script untuk scraping, cleaning, dan labeling
requirements.txt Dependensi modul data/ML
```

## Sumber Data

Daftar sumber berada di `data/raw/source_urls.txt`. Sumber dapat berupa:
- Public JSON API: Arbeitnow, Remotive, The Muse, Remote OK.
- Public HTML job listing pages: Dealls, Jobstreet Indonesia, LinkedIn public pages, dan sumber lain yang bisa diakses tanpa login.

Jika sebuah URL gagal, timeout, diblokir, membutuhkan login, captcha, paywall, atau struktur HTML tidak bisa diparse, proses tidak dibypass. Error disimpan di `data/raw/scraping_errors.csv` dan proses lanjut ke URL berikutnya.

## Menjalankan Modul Data

Instalasi dependensi:
```powershell
pip install -r requirements.txt
```

Jika `data/raw/scraped_job_posts.csv` sudah ada dan berisi data real, jangan jalankan scraping ulang agar dataset tidak tertimpa. Jalankan scraping hanya jika raw dataset belum ada atau memang ingin refresh data publik:
```powershell
python scraping/scraper_public_jobs.py
```

Jalankan cleaning dan labeling:
```powershell
python scraping/clean_and_label_data.py
```

Jalankan notebook visualisasi:
```powershell
python -m nbconvert --to notebook --execute --inplace notebooks/01_lokerlens_eda_and_visualization.ipynb --ExecutePreprocessor.timeout=180
```

## Output Modul Data

- `data/raw/scraped_job_posts.csv`
- `data/raw/scraping_errors.csv`
- `data/raw/raw_collection_log.csv`
- `data/processed/lokerlens_dataset_clean.csv`
- `data/processed/lokerlens_dataset_labeled.csv`
- `data/processed/red_flag_summary.csv`
- `figures/*.png`
- `reports/insight_summary.md`
- `reports/data_dictionary.md`

## Etika Scraping

Scraper hanya mengambil data dari sumber publik yang aman diakses. Project ini tidak melakukan login otomatis, tidak melewati captcha, tidak melewati paywall, dan tidak melakukan bypass keamanan. Informasi sensitif seperti email personal, nomor telepon, OTP, password, nomor rekening, atau nomor identitas tidak disimpan mentah dan dinormalisasi menjadi label kategori.

## Keterbatasan Data

Jumlah data bergantung pada ketersediaan sumber publik saat script dijalankan. Beberapa situs dapat membatasi request, mengubah struktur HTML, atau menolak akses otomatis. Label risiko dan trust score bersifat rule-based sehingga hasilnya digunakan sebagai indikasi awal, bukan keputusan mutlak bahwa sebuah lowongan aman atau berbahaya.
