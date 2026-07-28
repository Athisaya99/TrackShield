# from roboflow import Roboflow
# rf = Roboflow(api_key="UcqObxqPmbQVYIp2j7Uc")
# project = rf.workspace("dfsfsd").project("railway-foreign-object-detection-2va6t")
# version = project.version(1)
# dataset = version.download("yolov12")



#python 312           

from ultralytics import YOLO

# Path to your downloaded dataset YAML file (contains paths for train, val, names)
dataset_yaml_path = r"C:\Users\amaya\Desktop\Railway-obstacle-detection-main\mdit_foreignobjects\Railway-foreign-object-detection-1\data.yaml"

# Load the YOLOv8 (or YOLOv12 if available) model - starting from a pre-trained checkpoint
model = YOLO("yolov8n.pt")  # Use yolov8n.pt as a base; change to yolov12.pt when available

# Train the model
model.train(
    data=dataset_yaml_path,  # dataset config yaml
    epochs=50,
    batch=16,
    imgsz=640,
    device='cpu',  # change to -1 for CPU
    lr0=0.01,
    project="runs/train",
    name="railway_foreign_object_detection",
    exist_ok=True,
)
