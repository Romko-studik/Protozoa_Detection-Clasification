from ultralytics import YOLO

# Load the trained model
trained_model_path = 'runs/detect/train/weights/best.pt'
model = YOLO(trained_model_path)

# Run inference on a single image (replace with your own image path)
results = model.predict('path/to/your/image.jpg')

# Print predictions
results.show()  # Display the image with bounding boxes
results.save()  # Save the image with bounding boxes
