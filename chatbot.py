from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from config import PROMPT_SISTEMA
import os

# ✅ Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

# ✅ Inicializar cliente OpenAI
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# ✅ Inicializar FastAPI solo UNA vez
app = FastAPI()

# ✅ Configurar CORS correctamente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5501"],  # Dirección del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Modelo de datos esperado en la solicitud
class Pregunta(BaseModel):
    pregunta: str

# ✅ Ruta de la API
@app.post("/chat")
def obtener_respuesta(p: Pregunta):
    try:
        print("💬 Pregunta recibida:", p.pregunta)

        response = client.chat.completions.create(
            model="mistralai/mistral-small-3.1-24b-instruct:free",
            messages=[
                {"role": "system", "content": PROMPT_SISTEMA},
                {"role": "user", "content": p.pregunta}
            ],
            stream=False
        )

        # Adaptar según cómo responda tu modelo
        if hasattr(response.choices[0], "message"):
            respuesta = response.choices[0].message.content.strip()
        else:
            respuesta = response.choices[0].text.strip()

        print("🤖 Respuesta de la IA:", respuesta)

        if not respuesta:
            respuesta = "Lo siento, no encontré una respuesta. ¿Podrías reformular tu pregunta?"

        return {"respuesta": respuesta}

    except Exception as e:
        print("❌ Error:", str(e))
        raise HTTPException(status_code=500, detail="Error al conectarse con la IA: " + str(e))
