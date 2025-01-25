from ultralytics import YOLO

# Load a model
#model = YOLO("yolov8n.pt")  # load the pretrained model on coco dataset for first iteration

# Load a pretrained model
model_path = '/hpc/home/valerio.tiri/LABORS/adas_sviro/runs/detect/train3/weights/last.pt'
model = YOLO(model_path)

# Use the model
model.train(data="config.yaml", epochs=20)  # train the model
