import streamlit as st
from groq import Groq
import pdfplumber
import io
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY", "")

# ── Konfigurasi Halaman ──────────────────────────────────────────
st.set_page_config(
    page_title="CareerFit - CV Analyzer",
    page_icon="✨",
    layout="centered"
)

# ── Custom CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    /* Sembunyikan UI default Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Layout styling minimalis */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    /* Sembunyikan avatar icon bawaan streamlit untuk chat */
    .stChatMessageAvatar {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.title("Pengaturan")
    st.subheader("Upload Dokumen")
    uploaded_file = st.file_uploader("Pilih CV (PDF / TXT)", type=["pdf", "txt"])

    st.divider()
    st.caption("Panduan:\n1. Upload file CV Anda di atas\n2. Ketik posisi yang diminati atau ceritakan pengalaman Anda\n3. Biarkan sistem menganalisis kecocokannya")

# ── Judul ────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align: center; font-weight: 600; color: #2E3B4E; font-size: 2.5rem; margin-bottom: 0;'>CareerFit</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666666; font-size: 1.1rem;'>Analisis CV Anda & temukan peran LinkedIn yang paling relevan</p>", unsafe_allow_html=True)
st.divider()

# ── Baca CV ──────────────────────────────────────────────────────
cv_text = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            cv_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    else:
        cv_text = uploaded_file.read().decode("utf-8", errors="ignore")
    st.success(f"✅ CV berhasil dibaca: **{uploaded_file.name}**")

# ── System Prompt ─────────────────────────────────────────────────
from datetime import datetime

today = datetime.now().strftime("%d %B %Y")  # contoh: 04 September 2026

SYSTEM_PROMPT = f"""Kamu adalah AI CV Screener & Career Advisor. Tugasmu:
1. Menganalisis CV atau profil yang diberikan pengguna (skill, pengalaman, pendidikan).
2. Merekomendasikan 3-5 Posisi Pekerjaan (Job Titles) yang paling relevan untuk dicari di LinkedIn.
   - PENTING: JANGAN mengarang (berhalusinasi) tentang lowongan spesifik dari perusahaan tertentu yang seolah-olah sedang buka saat ini, karena kamu tidak memiliki akses internet real-time.
   - Fokus berikan rekomendasi POSISI PEKERJAAN secara umum yang cocok dengan profil pengguna.
3. Untuk setiap rekomendasi posisi, berikan:
   - 💼 Nama Posisi (contoh: QA Engineer, Data Analyst)
   - 📊 Persentase kecocokan dengan CV (contoh: 87%)
   - ✅ Alasan singkat mengapa skill/pengalaman di CV sangat cocok untuk posisi ini
   - 🔗 Link Pencarian LinkedIn: https://www.linkedin.com/jobs/search/?keywords=NAMA+POSISI&location=Indonesia (Ganti NAMA+POSISI dengan posisi yang disarankan, gunakan format URL encoding seperti %20 atau + untuk spasi)

Format rapi menggunakan markdown. Jawab dalam Bahasa Indonesia."""

# ── Inisialisasi Riwayat Chat ─────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Selamat datang di **CareerFit**.\n\n"
                "Sistem ini dirancang secara khusus untuk:\n"
                "- Menganalisis profil dan pengalaman pada CV Anda\n"
                "- Merekomendasikan peran pekerjaan yang relevan di LinkedIn\n"
                "- Memberikan metrik kecocokan objektif beserta alasannya\n\n"
                "Silakan unggah dokumen CV Anda melalui sidebar atau ceritakan profil Anda untuk memulai."
            )
        }
    ]

# ── Tampilkan Riwayat ─────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Input Chat ────────────────────────────────────────────────────
user_input = st.chat_input("Ceritakan pengalaman/skill Anda, atau minta rekomendasi pekerjaan...")

if user_input:
    if not api_key:
        st.warning("⚠️ Masukkan Groq API Key di sidebar terlebih dahulu.")
        st.stop()

    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gabungkan CV jika ada
    full_message = user_input
    if cv_text:
        full_message = f"Berikut isi CV saya:\n\n{cv_text[:3000]}\n\n---\nPertanyaan: {user_input}"

    # Bangun history untuk Groq (tanpa pesan selamat datang)
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in st.session_state.messages[1:-1]:  # skip welcome & pesan user terakhir
        history.append({"role": msg["role"], "content": msg["content"]})
    history.append({"role": "user", "content": full_message})

    # Panggil Groq API
    try:
        client = Groq(api_key=api_key)

        with st.chat_message("assistant"):
            with st.spinner("🔍 Menganalisis CV & mencari lowongan..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=history,
                    temperature=0.7,
                    max_tokens=2048,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"❌ Error: {e}")
