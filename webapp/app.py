import os
import json
import torch
from flask import Flask, request, jsonify, render_template
from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'models', 'chilidoc_vit_model')
TREATMENT_DATA_PATH = os.path.join(BASE_DIR, 'treatment_data.json')


CLASS_NAMES = [
    'Bacterial_Spot',
    'Cercospora_Leaf_Spot',
    'Curl_Virus',
    'Healthy_Leaf',
    'Nutrition_Deficiency',
    'White_Spot'
]

def normalize_class_name(class_name):
    if 'Healthy' in class_name:
        return 'Healthy'
    return class_name

print("Loading ViT model... this may take a moment.")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

processor = ViTImageProcessor.from_pretrained(MODEL_PATH)
model = ViTForImageClassification.from_pretrained(MODEL_PATH)
model.to(device)
model.eval()

with open(TREATMENT_DATA_PATH, 'r', encoding='utf-8') as f:
    treatment_data = json.load(f)

print("Model loaded successfully. ChiliDoc is ready.")


@app.route('/')
def home():
    return render_template('dashboard.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']

    try:
        image = Image.open(file.stream).convert('RGB')
    except Exception:
        return jsonify({'error': 'Invalid image file'}), 400

    inputs = processor(image, return_tensors="pt")
    pixel_values = inputs['pixel_values'].to(device)

    with torch.no_grad():
        outputs = model(pixel_values=pixel_values)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        confidence, predicted_idx = torch.max(probs, dim=1)

    predicted_class = CLASS_NAMES[predicted_idx.item()]
    lookup_key = normalize_class_name(predicted_class)

    info = treatment_data.get(lookup_key)

    if info is None:
        return jsonify({'error': f'No treatment data found for {predicted_class}'}), 500

    response = {
        'disease': lookup_key,
        'confidence': round(confidence.item() * 100, 2),
        'title': info['title'],
        'cause': info['cause'],
        'quick_tip': info['quick_tip'],
        'page': info['page']
    }

    return jsonify(response)


@app.route('/disease/<page_name>')
def disease_detail(page_name):
    # Basic safety check - only allow known html pages
    valid_pages = [v['page'] for v in treatment_data.values()]
    if page_name not in valid_pages:
        return "Page not found", 404
    return render_template(page_name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)