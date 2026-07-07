# Insight Summary

## Ringkasan Dataset

Dataset final berisi 300 lowongan real hasil public data collection setelah deduplikasi dan pembatasan maksimal 300 data. Rata-rata Trust Score adalah 68.1.

## Jumlah Data Hasil Scraping

- arbeitnow: 200 lowongan
- themuse: 72 lowongan
- remotive: 28 lowongan

## Sumber Data

Data berasal dari public job APIs yang dapat diakses tanpa login, yaitu Arbeitnow, Remotive, dan The Muse. URL tambahan dari `data/raw/source_urls.txt` dapat digunakan jika user memiliki halaman publik yang aman untuk diparse.

## Insight Utama

- Kompensasi tidak disebutkan muncul pada 211 lowongan, sehingga transparansi imbalan menjadi isu utama untuk proses apply.
- Jam kerja tidak jelas atau tidak disebutkan muncul pada 251 lowongan, yang membuat estimasi beban kerja perlu diklarifikasi.
- Sumber data terbesar berasal dari arbeitnow dengan 200 lowongan, sehingga interpretasi platform harus mempertimbangkan dominasi sumber tersebut.
- Red flag paling sering adalah working_hours_missing dengan 251 kemunculan.
- Risk level dengan Trust Score rata-rata terendah adalah Risiko Tinggi (32.0), menunjukkan hubungan missing information dan red flag terhadap skor.

## Critical Analysis

Mahasiswa, fresh graduate, dan freelancer pemula rentan terhadap lowongan tidak transparan karena sering membutuhkan pengalaman awal dan belum selalu punya pembanding proses rekrutmen yang sehat. Informasi kompensasi, jam kerja, kontrak, kontak resmi, dan supervisor penting karena menentukan beban kerja, batas komitmen, dan keamanan data pelamar. Permintaan data pribadi atau pembayaran terlalu awal perlu diperlakukan sebagai indikasi risiko yang harus diverifikasi.

## Implikasi untuk Fitur LokerLens

Hasil EDA mendukung Trust Score, Missing Information Checker, Red Flag Detector, Safe Apply Checklist, dan Recruiter Question Generator. Pola missing information dapat langsung diubah menjadi pertanyaan klarifikasi untuk recruiter.

## Implikasi untuk BMC

Insight data memperkuat value proposition berupa alat bantu membaca risiko lowongan, customer segment mahasiswa dan pencari kerja pemula, key activity berupa pengumpulan data dan rule-based risk analysis, serta channel edukasi digital melalui website LokerLens.

## Keterbatasan Data

Dataset bergantung pada ketersediaan public API saat scraping dijalankan. Beberapa lowongan global tidak selalu spesifik untuk magang atau entry-level, sehingga interpretasi perlu disesuaikan dengan konteks LokerLens. Scoring masih rule-based dan bukan pengganti validasi manusia.

## Catatan Etika Data

Modul ini tidak melakukan login, tidak melewati captcha, tidak melewati paywall, dan tidak menyimpan detail personal sensitif secara mentah. Jika data sensitif terdeteksi, data dinormalisasi menjadi kategori indikasi seperti `personal_email`, `whatsapp_personal`, atau `sensitive_data_detected`.
