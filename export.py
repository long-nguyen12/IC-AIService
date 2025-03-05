# Load the YOLOv8 model
from ultralytics import YOLO


model = YOLO("weights/yolov8s-oiv7.pt")

# Export the model to ONNX format
model.export(format="onnx")  # creates 'yolov8n.onnx'