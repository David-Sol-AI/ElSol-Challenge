# Documento Técnico

## A. Análisis del requerimiento

- Se requiere transcribir audios en formato `.wav` o `.mp3`.
- La información debe estructurarse para consultas posteriores mediante un chatbot.
- Se eligió **Azure OpenAI** para transcripción, embeddings y respuestas porque está disponible y ofrece modelos de alta calidad.
- Se usa **FastAPI** para exponer endpoints REST.
- Se emplea **Qdrant** como base vectorial en memoria para almacenar las transcripciones y sus metadatos.

## B. Arquitectura propuesta

```
[Cliente] --(audio)-->/transcribe --(transcripción + extracción)--> [VectorStore]
[Cliente] --(pregunta)-->/chat --(búsqueda+LLM)--> respuesta
```

- **FastAPI** actúa como orquestador.
- **Azure OpenAI** Whisper transcribe el audio.
- **Qdrant** almacena embeddings y metadatos.
- El endpoint `/chat` recupera información relevante y genera la respuesta con un modelo de chat.


