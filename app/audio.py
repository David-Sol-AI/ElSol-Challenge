"""Audio processing utilities."""

from __future__ import annotations

import os
import re
import tempfile
import uuid
from fastapi import UploadFile

from .openai_utils import get_openai_client
from .vectorstore import VectorStore
from .models import TranscriptionResponse
from .config import settings


def extract_structured_info(text: str) -> dict[str, str]:
    """Extract basic structured information from a transcript.

    The function looks for simple patterns such as ``Nombre:``, ``Edad:`` and
    ``Diagnóstico:``. Values are returned exactly as they appear in the text.
    """

    patterns = {
        "nombre": r"nombre\s*[:\-]\s*(?P<value>[^\n]+)",
        "edad": r"edad\s*[:\-]\s*(?P<value>\d+)",
        "diagnostico": r"diagn[oó]stico\s*[:\-]\s*(?P<value>[^\n]+)",
    }
    data: dict[str, str] = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            data[key] = match.group("value").strip()
    return data


def transcribe_audio(file: UploadFile, store: VectorStore) -> TranscriptionResponse:
    """Transcribe an uploaded audio file and store the result in the vector DB."""

    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    client = get_openai_client()
    with open(tmp_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=settings.azure_openai_deployment,
            file=audio_file,
        )
        transcript = result.text

    os.remove(tmp_path)

    structured = extract_structured_info(transcript)
    doc_id = str(uuid.uuid4())
    store.add_document(doc_id, transcript, structured)

    return TranscriptionResponse(id=doc_id, transcript=transcript, structured_data=structured)
