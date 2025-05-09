from ultralytics import YOLO
import torch
import torch.multiprocessing as mp

def main():
    data_yaml_path = '../data/data.yaml'


    model = YOLO('yolov8n.pt')
    print(torch.cuda.is_available())
    print(torch.cuda.device_count()) 
    print(torch.cuda.current_device())  

    model.train(data=data_yaml_path, epochs=50, imgsz=640, device='0', workers=8, batch=12, project='runs/train', name='yolov8n_custom', exist_ok=True,half =True, optimizer='adam')
if __name__ == "__main__":
    mp.set_start_method('spawn', force=True)

    main()