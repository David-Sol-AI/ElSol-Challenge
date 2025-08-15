"""FastAPI application exposing transcription and chat endpoints."""

from fastapi import FastAPI, File, HTTPException, UploadFile

from .audio import transcribe_audio
from .models import ChatRequest, ChatResponse, TranscriptionResponse
from .vectorstore import VectorStore
from .openai_utils import get_openai_client
from .config import settings

app = FastAPI(title="ElSol Challenge API")

store = VectorStore()


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile = File(...)) -> TranscriptionResponse:
    """Transcribe an uploaded audio file (.wav or .mp3)."""

    if not file.filename.lower().endswith((".wav", ".mp3")):
        raise HTTPException(status_code=400, detail="Formato no soportado")
    return transcribe_audio(file, store)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Answer medical questions based on stored transcripts."""

    results = store.query(request.question)
    context = "\n".join(point.payload.get("text", "") for point in results)

    client = get_openai_client()
    messages = [
        {"role": "system", "content": "Eres un asistente médico."},
        {
            "role": "user",
            "content": f"Contexto:\n{context}\n\nPregunta: {request.question}",
        },
    ]

    completion = client.chat.completions.create(
        model=settings.azure_openai_deployment,
        messages=messages,
        temperature=0.7,
    )
    answer = completion.choices[0].message.content
    return ChatResponse(answer=answer)
