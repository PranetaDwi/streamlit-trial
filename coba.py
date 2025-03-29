import streamlit as st
import speech_recognition as sr
import tempfile
import os
from pydub import AudioSegment
from pydub.utils import which

# Pastikan ffmpeg dikenali oleh pydub
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffmpeg = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

# Debug: Cek apakah ffmpeg tersedia
if not AudioSegment.converter:
    st.error("Error: ffmpeg tidak ditemukan. Pastikan ffmpeg sudah terinstall di environment.")

st.title("🎤 Pengenalan Perintah Suara")

# Upload file suara
uploaded_file = st.file_uploader("📂 Upload file suara (M4A, MP3, WAV, OGG)", type=["m4a", "mp3", "wav", "ogg"])

if uploaded_file is not None:
    try:
        # Simpan file sementara
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(uploaded_file.read())  # Simpan file upload ke disk
            temp_file_path = temp_file.name  # Simpan path file

        # Konversi ke format WAV
        audio = AudioSegment.from_file(temp_file_path)
        output_path = temp_file_path.replace(".wav", "_converted.wav")
        audio.export(output_path, format="wav")

        # Tampilkan audio
        st.audio(output_path, format="audio/wav")

        # Speech Recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(output_path) as source:
            st.write("🛠️ Mengenali suara...")
            audio_data = recognizer.record(source)

            try:
                # Gunakan bahasa Indonesia
                command_text = recognizer.recognize_google(audio_data, language="id-ID")
                st.success(f"✅ Perintah yang dikenali: **{command_text}**")
            except sr.UnknownValueError:
                st.error("❌ Maaf, tidak dapat mengenali suara.")
            except sr.RequestError:
                st.error("❌ Gagal terhubung ke layanan Speech Recognition.")

        # Hapus file sementara
        os.remove(temp_file_path)
        os.remove(output_path)

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
