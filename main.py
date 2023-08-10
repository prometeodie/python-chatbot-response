from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from decouple import config
import openai

api_key = config("API_KEY")


app = FastAPI()

origins = [
  "http://localhost:4200",
  "http://127.0.0.1:8000"
]
app.add_middleware(
CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# TODO:configurar CORS
class Message(BaseModel):
  message:str

@app.post("/chatbot")
async def bot_response(message:Message):
  try:
    # Configura la clave API
      openai.api_key = api_key

    # Realiza una petición a la API
      prompt = message.message
      response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50  
      )
      return{response.choices[0].text.strip()}
  except openai.error.OpenAIError as e:
     # Captura el error específico de OpenAI y devuelve el mensaje de error
     error_message = e.response["error"]["message"]
     raise HTTPException(status_code=500, detail=error_message)

