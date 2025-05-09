from ultralytics import YOLO

trained_model_path = 'runs/train/yolov8n_custom/weights/best.pt'
data_yaml_path = '../data/data.yaml'  # Path to your data.yaml file

def main():
    model = YOLO(trained_model_path)

    metrics = model.val(data=data_yaml_path)
    print(metrics)

if __name__ == "__main__":
    main()