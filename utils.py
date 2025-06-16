import uuid
import os

UPLOAD_FOLDER = "uploads/images"
CAPTION_FOLDER = "uploads/images"
AUDIO_FOLDER = "audio"

def config(app):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    if not os.path.exists(AUDIO_FOLDER):
        os.makedirs(AUDIO_FOLDER, exist_ok=True)
    if not os.path.exists(CAPTION_FOLDER):
        os.makedirs(CAPTION_FOLDER, exist_ok=True)
        
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}
    app.config["AUDIO_FOLDER"] = AUDIO_FOLDER
    app.config["CAPTION_FOLDER"] = CAPTION_FOLDER

    

def file_extension(filename):
    if filename.endswith('.jpg'):
        return '.jpg'
    elif filename.endswith('.png'):
        return '.png'
    elif filename.endswith('.jpeg'):
        return '.jpeg'