# Data Dictionary

| Column | Type | Explanation | Example |
|---|---|---|---|
| `id` | integer | Nomor unik baris data. |  |
| `source_name` | string | Nama sumber public API atau public page. | arbeitnow |
| `source_platform` | string | Kategori platform sumber lowongan. | job_site |
| `source_url` | string | URL publik sumber lowongan. |  |
| `collected_at` | string | Collected at |  |
| `job_title` | string | Job title |  |
| `company_name` | string | Company name |  |
| `company_clarity` | string | Company clarity |  |
| `job_type` | string | Job type |  |
| `job_text` | string | Job text |  |
| `job_description` | string | Job description |  |
| `requirements` | string | Requirements |  |
| `benefits` | string | Benefits |  |
| `compensation_status` | string | Compensation status |  |
| `compensation_text` | string | Compensation text |  |
| `working_hours_status` | string | Working hours status |  |
| `working_hours_text` | string | Working hours text |  |
| `work_arrangement` | string | Work arrangement |  |
| `location` | string | Location |  |
| `duration_status` | string | Duration status |  |
| `duration_text` | string | Duration text |  |
| `contact_type` | string | Contact type |  |
| `asks_sensitive_data` | string | Asks sensitive data |  |
| `sensitive_data_terms` | string | Sensitive data terms |  |
| `asks_payment` | string | Asks payment |  |
| `payment_terms` | string | Payment terms |  |
| `unrealistic_promise` | string | Unrealistic promise |  |
| `unrealistic_promise_terms` | string | Unrealistic promise terms |  |
| `workload_status` | string | Workload status |  |
| `missing_fields` | string | Informasi penting yang tidak disebutkan, dipisahkan semicolon. |  |
| `red_flag_categories` | string | Kategori indikasi risiko berbasis rule-based. | compensation_missing;working_hours_missing |
| `red_flag_count` | integer | Red flag count |  |
| `trust_score` | integer | Skor 0-100 untuk transparansi dan indikasi risiko. | 84 |
| `risk_level` | string | Kategori risiko berdasarkan trust_score. | Cukup Aman, Tapi Perlu Dicek |
| `recommended_action` | string | Rekomendasi awal untuk pelamar. |  |
| `notes` | string | Notes |  |
