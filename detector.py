import os
from pathlib import Path
import sys
import cv2
from ultralytics import YOLO
from transformers import VitsModel, AutoTokenizer

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


def load_model():
    """Load a model from a file."""
    model = YOLO("weights/yolov8s-oiv7.onnx", task="detect")
    return model


def detect(frame, model, filename):
    try:
        result = model(frame)[0]
        bboxes = []
        boxes = (
            result.boxes.xyxy.int().tolist()
        )  # Boxes object for bounding box outputs
        clss = result.boxes.cls.int().tolist()
        scores = result.boxes.conf.float().tolist()
        cls_names = [str(model.names[cls_id]) for cls_id in clss]
        for xyxy, conf, cls_id, cls_name in zip(boxes, scores, clss, cls_names):
            result_dict = {
                "box": xyxy,
                "conf": round(conf, 2),
                "class_id": cls_id,
                "class_name": cls_name,
            }
            bboxes.append(result_dict)
        result.save(filename=filename)
        return bboxes
    except Exception as e:
        print(e)

def load_text2speech_model():
    model = VitsModel.from_pretrained("facebook/mms-tts-vie")
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-vie")
    return model, tokenizer