import os
import subprocess
import tempfile

from google.api_core.client_options import ClientOptions
from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


class SpeechToTextService:

    def __init__(self):
        self.client = speech_v2.SpeechClient(
            client_options=ClientOptions(
                api_endpoint="us-speech.googleapis.com"
            )
        )

    def transcribe(self, audio_bytes: bytes, file_extension: str) -> str:

        # Create temporary input and output files
        with tempfile.TemporaryDirectory() as temp_dir:

            input_path = os.path.join(
                temp_dir,
                f"input{file_extension}"
            )

            output_path = os.path.join(
                temp_dir,
                "converted.wav"
            )

            # Save uploaded audio
            with open(input_path, "wb") as audio_file:
                audio_file.write(audio_bytes)

            # Convert audio to:
            # 16 kHz
            # mono
            # 16-bit PCM WAV
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    input_path,
                    "-ac",
                    "1",
                    "-ar",
                    "16000",
                    "-sample_fmt",
                    "s16",
                    output_path,
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            # Read converted WAV
            with open(output_path, "rb") as wav_file:
                wav_content = wav_file.read()

        config = cloud_speech.RecognitionConfig(
            explicit_decoding_config=cloud_speech.ExplicitDecodingConfig(
                encoding=cloud_speech.ExplicitDecodingConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                audio_channel_count=1,
            ),
            language_codes=["ar-XA"],
            model="chirp_3",
        )

        request = cloud_speech.RecognizeRequest(
            recognizer=(
                f"projects/{PROJECT_ID}"
                "/locations/us/recognizers/_"
            ),
            config=config,
            content=wav_content,
        )

        response = self.client.recognize(request=request)

        transcripts = []

        for result in response.results:
            if result.alternatives:
                transcripts.append(
                    result.alternatives[0].transcript
                )

        return " ".join(transcripts)