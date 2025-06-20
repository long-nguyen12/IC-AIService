import os
import cv2
from flask import Flask, jsonify, logging, request, send_from_directory, send_file
from flask_cors import CORS
from detector import detect, load_model, load_text2speech_model
from utils import *
from werkzeug.utils import secure_filename
from voice_generator import generate_voice
from caption_generator import generate_cation

app = Flask(__name__)
CORS(app)

model = load_model()
tts_model, tts_tokenizer = load_text2speech_model()

config(app)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route("/v1/api/detection", methods=["POST"])
def detect_objects():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            image = cv2.imread(filepath)
            w, h, _ = image.shape
            
            filename = filename.lower()
            save_ext = file_extension(filename)
            save_path = filepath.replace(save_ext, f"_detection{save_ext}")
            detection_results = detect(image, model, save_path)

            bboxes = []
            for result_dict in detection_results:
                bbox_from_dict = BBox(
                            box=result_dict["box"],
                            conf=result_dict["conf"],
                            class_id=result_dict["class_id"],
                            class_name=result_dict["class_name"])
                bboxes.append(bbox_from_dict)

            return jsonify({"dectect_path": str(save_path)})
    except Exception as e:
        print(f"Error processing image: {e}")
        return f"Error processing image: {e}", 500

@app.route("/v1/api/images/<filename>", methods=["GET"])
def get_image(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/v1/api/text2speech", methods=["POST"])
def converttts():
    try:
        data = request.get_json()
    
        if not data or "message" not in data:
            return jsonify({"error": "Message is required"}), 400

        message = data["message"]
        
        filename = f"{uuid.uuid4().hex}.wav"
        filepath = os.path.join(app.config["AUDIO_FOLDER"], filename)
        try:
            generate_voice(filepath, message)
        except Exception as e:
            print(f"Error generating voice: {e}")
            return jsonify({"error": "Failed to generate voice"}), 500
        
        return jsonify({"audio_file": str(filename)})
    except Exception as e:
        print(f"Error processing image: {e}")
        return f"Error processing image: {e}", 500


@app.route("/v1/api/audio/<filename>", methods=["GET"])
def get_audio(filename):        
    filepath = os.path.join(app.config["AUDIO_FOLDER"], filename)
    return send_file(filepath, as_attachment=True, download_name=filename, mimetype="audio/wav")


@app.route("/v1/api/image2text", methods=["POST"])
def image2text():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["CAPTION_FOLDER"], filename)
            file.save(filepath)
            try:
                caption = generate_cation(filepath)
            except Exception as e:
                print(f"Error generating caption: {e}")
                return jsonify({"error": "Failed to generate caption"}), 500
            return jsonify({"generated_text": caption})
    except Exception as e:
        print(f"Error processing image: {e}")
        return f"Error processing image: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
