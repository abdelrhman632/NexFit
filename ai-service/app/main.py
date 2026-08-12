from fastapi import FastAPI, File, HTTPException, UploadFile

from app.services.speech_to_text import SpeechToTextService


app = FastAPI(
    title="NexFit AI Service",
    version="1.0.0"
)


speech_to_text_service = SpeechToTextService()


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }


@app.post("/api/speech-to-text")
async def speech_to_text(
    audio: UploadFile = File(...)
):
    try:
        audio_bytes = await audio.read()

        if not audio_bytes:
            raise HTTPException(
                status_code=400,
                detail="Audio file is empty."
            )

        filename = audio.filename or ""

        if "." not in filename:
            raise HTTPException(
                status_code=400,
                detail="Audio file must have an extension."
            )

        file_extension = "." + filename.rsplit(".", 1)[1].lower()

        transcript = speech_to_text_service.transcribe(
            audio_bytes,
            file_extension
        )

        if not transcript:
            raise HTTPException(
                status_code=422,
                detail="No speech could be detected."
            )

        return {
            "text": transcript
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Speech-to-text processing failed: {str(e)}"
        )