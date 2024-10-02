import os
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

def fine_tune_model(train_images, train_texts):
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    optimizer = torch.optim.Adam(model.parameters(), lr=5e-6)
    model.train()

    for epoch in range(3):
        for image_path, text in zip(train_images, train_texts):
            image = Image.open(image_path).convert("RGB")
            inputs = processor(text=text, images=image, return_tensors="pt", padding=True)

            outputs = model(**inputs)
            loss = outputs.loss

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            print(f"Epoch {epoch}, Loss: {loss.item()}")

    if not os.path.exists('models/fine_tuned'):
        os.makedirs('models/fine_tuned')

    model.save_pretrained("models/fine_tuned")
    processor.save_pretrained("models/fine_tuned")
    print("Fine-tuned model saved.")
