import streamlit as st
import speech_recognition as sr
import tempfile
import os

st.title("Pengenalan Perintah Suara")

recognizer = sr.Recognizer()
microphone = sr.Microphone()

if "recording" not in st.session_state:
    st.session_state["recording"] = False
if "file_path" not in st.session_state:
    st.session_state["file_path"] = None

with microphone as source:
    st.write("Silakan berbicara...")
    recognizer.adjust_for_ambient_noise(source) 
    audio_data = recognizer.listen(source)
    
    try:
        command_text = recognizer.recognize_google(audio_data, language="id-ID")
        st.success(f"Perintah yang dikenali: **{command_text}**")
    except sr.UnknownValueError:
        st.error("Maaf, tidak dapat mengenali suara.")
    except sr.RequestError:
        st.error("Gagal terhubung ke layanan Speech Recognition.")