# ======================================================
# 🤖 ChatAI Pro FLUX 2025 — Groq + Voce + Immagini (HuggingFace Router)
# ======================================================

import gradio as gr
import requests, io, base64, tempfile, os
from deep_translator import GoogleTranslator
from PIL import Image
import speech_recognition as sr
from gtts import gTTS

# ======================================================
# 🔑 CHIAVI API (da impostare come variabili d’ambiente su Render)
# ======================================================
API_KEY = os.getenv("GROQ_API_KEY")   # ← Inserisci su Render la tua chiave Groq
HF_TOKEN = os.getenv("HF_TOKEN")      # ← Inserisci su Render la tua chiave Hugging Face

conversation_history = []

# ======================================================
# 🔍 Verifica Token Hugging Face
# ======================================================
def check_hf_token():
    test_prompt = "a smiling cat wearing sunglasses"
    url = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    r = requests.post(url, headers=headers, json={"inputs": test_prompt})
    if r.status_code == 200:
        return "✅ Token Hugging Face valido!"
    elif r.status_code == 401:
        return "❌ Token Hugging Face non valido o senza permessi Inference API!"
    else:
        return f"⚠️ Errore Hugging Face: {r.status_code} - {r.text[:150]}"

# ======================================================
# 💬 Chat AI con memoria e traduzione
# ======================================================
def chat_ai(message, language):
    global conversation_history
    try:
        if any(word in message.lower() for word in ["immagine", "disegna", "crea", "picture", "foto"]):
            return generate_image(message)

        conversation_history.append({"role": "user", "content": message})
        headers = {"Authorization": f"Bearer {API_KEY}"}
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "Rispondi come un assistente amichevole e utile."}
            ] + conversation_history,
            "temperature": 0.7,
            "max_tokens": 700
        }

        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                          headers=headers, json=data, timeout=60)

        if r.status_code == 200:
            text = r.json()["choices"][0]["message"]["content"].strip()
            if language != "it":
                text = GoogleTranslator(source="auto", target=language).translate(text)
            conversation_history.append({"role": "assistant", "content": text})
            return text
        else:
            return f"❌ Errore {r.status_code}: {r.text}"
    except Exception as e:
        return f"❌ Errore: {str(e)}"

# ======================================================
# 🎨 Generatore immagini
# ======================================================
def generate_image(prompt):
    try:
        hf_url = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
        hf_headers = {"Authorization": f"Bearer {HF_TOKEN
