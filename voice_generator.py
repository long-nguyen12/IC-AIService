import os
from google import genai
from google.genai import types
import wave
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)
print("API Key:", api_key)


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

# Set up the wave file to save the output:
def generate_voice(filename, audio_content):
    response = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents=audio_content,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name='Kore',
                )
            )
        ),
    )
    )
    data = response.candidates[0].content.parts[0].inline_data.data
    file_name=filename
    wave_file(file_name, data)