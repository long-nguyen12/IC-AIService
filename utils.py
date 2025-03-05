import uuid
import os

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "audio"

def config(app):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(AUDIO_FOLDER, exist_ok=True)
        
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}
    app.config["AUDIO_FOLDER"] = AUDIO_FOLDER

    

def file_extension(filename):
    if filename.endswith('.jpg'):
        return '.jpg'
    elif filename.endswith('.png'):
        return '.png'
    elif filename.endswith('.jpeg'):
        return '.jpeg'