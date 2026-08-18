import os

from google.api_core.client_options import ClientOptions
from google.cloud import speech_v2
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
AUDIO_FILE = r"C:\Users\Abdelrhman Yasser\Desktop\NexFit\ai-service\test_audio.wav"

def transcribe_audio():
    print("Starting Speech-to-Text test...")
    print(f"Project: {PROJECT_ID}")
    print(f"Audio file: {AUDIO_FILE}")

    client = SpeechClient(
        client_options=ClientOptions(
            api_endpoint="us-speech.googleapis.com"
        )
    )

    with open(AUDIO_FILE, "rb") as audio_file:
        audio_content = audio_file.read()

    print(f"Audio size: {len(audio_content)} bytes")
    print("Sending audio to Google Speech-to-Text...")

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
        recognizer=f"projects/{PROJECT_ID}/locations/us/recognizers/_",
        config=config,
        content=audio_content,
    )

    response = client.recognize(request=request)

    print("\nResponse received:")
    print(response)

    print("\n" + "=" * 50)
    print("TRANSCRIPTION")
    print("=" * 50)

    if not response.results:
        print("No transcription results were returned.")
        return

    for result in response.results:
        if result.alternatives:
            print(result.alternatives[0].transcript)
        else:
            print("A result was returned, but it contains no alternatives.")


if __name__ == "__main__":
    transcribe_audio()