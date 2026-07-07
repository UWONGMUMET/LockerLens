import {
  AlertTriangle,
  BadgeCheck,
  ClipboardCheck,
  Eye,
  FileWarning,
  HelpCircle,
  ListChecks,
  SearchCheck,
  ShieldCheck,
} from 'lucide-react';

export const features = [
  {
    title: 'Trust Score',
    description: 'Skor 0-100 untuk membaca seberapa transparan dan layak diverifikasi sebuah lowongan.',
    icon: ShieldCheck,
  },
  {
    title: 'Red Flag Detection',
    description: 'Mendeteksi indikasi seperti biaya pendaftaran, permintaan data sensitif, atau janji yang terlalu tinggi.',
    icon: AlertTriangle,
  },
  {
    title: 'Missing Information Check',
    description: 'Menandai detail yang belum muncul, seperti kompensasi, jam kerja, durasi, lokasi, dan supervisor.',
    icon: FileWarning,
  },
  {
    title: 'Safe Apply Checklist',
    description: 'Checklist praktis agar kamu tahu apa yang perlu dicek sebelum mengirim lamaran.',
    icon: ClipboardCheck,
  },
];

export const problemItems = [
  'Gaji, fee, atau uang saku tidak disebutkan dengan jelas.',
  'Jobdesc terlalu luas sehingga batas tanggung jawab sulit dibaca.',
  'Benefit hanya ditulis umum tanpa detail pembelajaran atau kompensasi.',
  'Workload, jam kerja, dan durasi program tidak transparan.',
  'Data pribadi diminta terlalu awal sebelum kanal resmi terverifikasi.',
];

export const safetyChecklist = [
  'Cek nama perusahaan, website resmi, dan email domain perusahaan.',
  'Pastikan kompensasi, jam kerja, durasi, dan jobdesc tertulis jelas.',
  'Simpan bukti komunikasi dan dokumen penawaran.',
  'Tanyakan supervisor, mentor, atau PIC yang bertanggung jawab.',
  'Jangan membayar biaya pendaftaran, deposit, atau administrasi rekrutmen.',
  'Jangan memberikan OTP, password, PIN, atau foto identitas sebelum proses resmi jelas.',
];

export const sensitiveData = [
  'KTP atau foto kartu identitas',
  'Nomor rekening sebelum kontrak jelas',
  'OTP, PIN, atau password',
  'Selfie dengan kartu identitas',
  'Kartu keluarga',
];

export const recruiterQuestions = [
  'Berapa range kompensasi, fee, gaji, atau uang saku?',
  'Bagaimana jam kerja, format kerja, dan estimasi workload mingguan?',
  'Apa jobdesc utama, target kerja, dan kualifikasi wajib?',
  'Berapa durasi program atau kontrak kerja?',
  'Siapa supervisor, mentor, atau PIC harian?',
  'Apakah ada kontrak, offer letter, atau dokumen resmi?',
];

export const redFlagExamples = [
  'Ada biaya pendaftaran, deposit, atau admin rekrutmen.',
  'Janji penghasilan tidak realistis tanpa struktur kompensasi.',
  'Nama perusahaan, alamat, dan kanal resmi tidak jelas.',
  'Jobdesc ambigu seperti mengerjakan semua tugas.',
  'Unpaid tetapi workload terlihat berat atau full-time.',
];

export const verificationTips = [
  'Cocokkan lowongan dengan website resmi perusahaan.',
  'Cek apakah email recruiter memakai domain perusahaan.',
  'Lihat LinkedIn company page dan aktivitas karyawan.',
  'Verifikasi alamat kantor dan kanal kontak resmi.',
  'Baca review karyawan dari beberapa sumber, bukan satu sumber saja.',
];

export const sampleJobText = `PT Cerah Digital membuka Program Internship Social Media selama 3 bulan.

Tanggung jawab:
- Membuat kalender konten Instagram dan TikTok
- Menulis caption dan membantu reporting performa mingguan
- Berkoordinasi dengan mentor marketing

Kualifikasi:
- Mahasiswa tingkat akhir atau fresh graduate
- Bisa menggunakan Canva dan memahami tren media sosial

Benefit:
- Uang saku Rp1.500.000 per bulan
- Sertifikat dan feedback portofolio

Jam kerja Senin-Jumat 09.00-17.00, hybrid 2 hari WFO di Jakarta Selatan.
Kirim CV dan portofolio ke internship@cerahdigital.co.id.`;

export const exampleResult = {
  score: 72,
  level: 'Cukup Aman, Tapi Perlu Dicek',
  redFlags: ['Jam kerja belum detail', 'Benefit masih perlu diverifikasi'],
  missing: ['Durasi kontrak', 'Supervisor harian'],
};

export const scannerSteps = [
  { title: 'Paste teks lowongan', icon: Eye },
  { title: 'Pilih konteks lowongan', icon: HelpCircle },
  { title: 'Baca rekomendasi aman', icon: SearchCheck },
  { title: 'Apply lebih kritis', icon: BadgeCheck },
  { title: 'Simpan checklist', icon: ListChecks },
];
