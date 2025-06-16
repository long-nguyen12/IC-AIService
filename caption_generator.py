from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

def generate_cation(image_path):
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg',
            ),
            "Sinh mô tả khoảng 15-20 từ cho bức ảnh này. Đầu ra chỉ bao gồm dòng mô tả."
        ]
    )

    return response.text