# 🤖 AI CV Screening Chatbot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-screening-cv.streamlit.app/)

Coba aplikasinya langsung di sini: **[https://ai-screening-cv.streamlit.app/](https://ai-screening-cv.streamlit.app/)**

## 📖 Tentang Aplikasi
**AI CV Screener** adalah chatbot interaktif cerdas yang ditenagai oleh AI (Groq API) untuk membantu menganalisis Curriculum Vitae (CV) Anda dan memberikan rekomendasi peran pekerjaan *(job roles)* yang paling relevan.

Aplikasi ini tidak hanya merekomendasikan nama posisi, tetapi juga memberikan alasan kecocokan, persentase metrik kesesuaian, dan **tautan pencarian otomatis ke LinkedIn Indonesia**.

## 🎯 Untuk Siapa Aplikasi Ini?
Aplikasi ini sangat cocok digunakan oleh:
- **Fresh Graduates (Lulusan Baru)** yang masih bingung menentukan arah karir atau posisi pekerjaan apa yang paling cocok dengan bekal keahlian mereka.
- **Job Seekers (Pencari Kerja)** yang ingin mengevaluasi kecocokan CV mereka sebelum melamar posisi tertentu.
- **Profesional (Career Switchers)** yang ingin berpindah karir dan ingin tahu peluang peran apa saja yang relevan dengan pengalaman mereka saat ini.

## 🔄 Alur Flow Aplikasi (Cara Kerja)
1. **Upload CV:** Pengguna mengunggah dokumen CV mereka dalam format PDF atau TXT di sidebar aplikasi. (Opsional: pengguna juga bisa langsung mengetikkan pengalaman mereka di kolom chat).
2. **Ekstraksi Data:** Sistem membaca dan mengekstrak teks serta informasi penting dari dokumen yang diunggah.
3. **Analisis AI:** Chatbot (menggunakan prompt cerdas) menganalisis keterampilan, pendidikan, dan pengalaman pengguna.
4. **Hasil Rekomendasi:** AI membalas dengan memberikan:
   - 💼 **3-5 Rekomendasi Posisi Pekerjaan** yang paling cocok.
   - 📊 **Persentase Kecocokan** untuk masing-masing posisi.
   - ✅ **Alasan Singkat** mengapa profil pengguna cocok untuk posisi tersebut.
   - 🔗 **Tautan (Link) Pencarian LinkedIn**, yang jika diklik akan langsung mencari lowongan posisi tersebut di LinkedIn (area Indonesia).

## 🛠️ Teknologi yang Digunakan
- **[Streamlit](https://streamlit.io/):** Framework untuk antarmuka web interaktif.
- **[Groq AI](https://groq.com/):** Engine LLM berkecepatan tinggi untuk pemrosesan NLP.
- **PDFPlumber:** Ekstraksi teks akurat dari file PDF.

## 🚀 Menjalankan Secara Lokal
Jika Anda ingin menjalankan proyek ini di komputer Anda sendiri:
1. Clone repository ini.
2. Install dependencies: `pip install -r requirements.txt`
3. Buat file `.env` dan masukkan API Key Groq Anda:
   ```env
   GROQ_API_KEY="api_key_anda"
   ```
4. Jalankan aplikasi: `streamlit run app.py`
