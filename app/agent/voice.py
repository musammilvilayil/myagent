from __future__ import annotations

import tempfile
from pathlib import Path

from app.config import settings

_model = None


def transcribe_audio(audio: bytes) -> dict:
    global _model
    if not audio:
        return {"ok": False, "error": "No audio data was received."}
    if len(audio) > 25 * 1024 * 1024:
        return {"ok": False, "error": "Audio upload exceeds the 25 MB limit."}
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("Local voice transcription is optional. Install requirements-voice.txt first.") from exc
    if _model is None:
        _model = WhisperModel(settings.whisper_model, device="cpu", compute_type="int8")
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as temp:
        temp.write(audio)
        audio_path = Path(temp.name)
    try:
        segments, info = _model.transcribe(str(audio_path), vad_filter=True, beam_size=3)
        transcript = " ".join(segment.text.strip() for segment in segments).strip()
        return {"ok": bool(transcript), "text": transcript, "language": info.language,
                "language_probability": round(info.language_probability, 3)}
    finally:
        audio_path.unlink(missing_ok=True)
