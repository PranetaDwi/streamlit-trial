os.system("pip install speechrecognition pydub ffmpeg")
import streamlit as st
import speech_recognition as sr
import tempfile
import os
from pydub import AudioSegment
from pydub.utils import which

# Pastikan ffmpeg dikenali oleh pydub
AudioSegment.converter = which("ffmpeg")

st.title("Pengenalan Perintah Suara")

# Upload file suara
uploaded_file = st.file_uploader("Upload file suara (M4A, MP3, WAV, OGG)", type=["m4a", "mp3", "wav", "ogg"])

if uploaded_file is not None:
    # Simpan file sementara
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        file_path = temp_file.name
        audio = AudioSegment.from_file(uploaded_file)
        audio.export(file_path, format="wav")  # Konversi ke WAV

    # Tampilkan audio
    st.audio(file_path, format="audio/wav")

    # Speech Recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        st.write("Mengenali suara...")
        audio_data = recognizer.record(source)

        try:
            # Gunakan bahasa Indonesia
            command_text = recognizer.recognize_google(audio_data, language="id-ID")
            st.success(f"Perintah yang dikenali: {command_text}")
        except sr.UnknownValueError:
            st.error("Maaf, tidak dapat mengenali suara.")
        except sr.RequestError:
            st.error("Gagal terhubung ke layanan Speech Recognition.")

    # Hapus file sementara
    os.remove(file_path)