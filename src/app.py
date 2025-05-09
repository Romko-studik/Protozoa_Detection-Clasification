from flask import Flask, request, jsonify, render_template
import torch
from PIL import Image
from io import BytesIO
from ultralytics import YOLO
from flask_cors import CORS
import os

device = torch.device('cpu')
model = YOLO('runs/train/yolov8n_custom/weights/best.pt').to(device)

app = Flask(__name__)
CORS(app)  

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        img = Image.open(BytesIO(file.read()))
        
        results = model(img)

        predictions = []
        for result in results:
            for detection in result.boxes.data.cpu().numpy():
                label_idx = int(detection[5])  
                confidence = float(detection[4]) 
                x1, y1, x2, y2 = map(float, detection[:4])  
                
                if label_idx < len(model.names):
                    label_name = model.names[label_idx]
                else:
                    label_name = "Unknown"

                predictions.append({
                    'label': label_name,
                    'confidence': confidence,
                    'bbox': [x1, y1, x2, y2]
                })

        labels = model.names 

        print("Predictions: ", predictions)
        if not predictions:
            return jsonify({'message': 'No objects detected.'}), 200  
        return jsonify({
            'predictions': predictions,
            'labels': labels
        })
    except Exception as e:
        return jsonify({'error': str(e)})





if __name__ == '__main__':
    print("Model labels:", model.names)
    app.run(debug=True)
