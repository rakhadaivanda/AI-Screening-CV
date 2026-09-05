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
    page_title="AI CV Screener",
    page_icon="🤖",
    layout="centered"
)

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Pengaturan")
    st.subheader("📄 Upload CV")
    uploaded_file = st.file_uploader("Upload CV (PDF / TXT)", type=["pdf", "txt"])

    st.divider()
    st.caption("Cara pakai:\n1. Upload CV (PDF/TXT) di atas\n2. Ketik pengalaman atau pertanyaan Anda\n3. Kirim pesan ke chatbot")

# ── Judul ────────────────────────────────────────────────────────
st.title("🤖 AI CV Screening Chatbot")
st.caption("Analisis CV Anda & temukan lowongan LinkedIn yang paling cocok")

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
                "👋 Halo! Saya **AI CV Screener** berbasis Groq AI.\n\n"
                "Saya bisa:\n"
                "- 📄 Menganalisis CV Anda\n"
                "- 🔍 Merekomendasikan lowongan LinkedIn yang cocok\n"
                "- 📊 Memberikan **persentase kecocokan** & alasannya\n\n"
                "Silakan **upload CV** di sidebar atau ceritakan pengalaman Anda!"
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
