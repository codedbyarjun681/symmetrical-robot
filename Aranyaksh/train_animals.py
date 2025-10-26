from ultralytics import YOLO
import torch 


def train_model():
    
    model = YOLO('yolov8n.pt')

    
    results = model.train(
        data='data.yaml',
        epochs=50,                  
        imgsz=640,                  
        project='training_results', 
        name='animal_expert_v1'     
    )
    print("Training complete! Your new model is saved in 'training_results/animal_expert_v1'.")

if __name__ == '__main__':
    
    print(f"Is CUDA available? {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Current device: {torch.cuda.get_device_name(torch.cuda.current_device())}")
    
   
    train_model()