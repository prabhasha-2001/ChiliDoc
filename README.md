# ChiliDoc

## AI-Based Chili Leaf Disease Detection and Treatment Recommendation System

ChiliDoc is an AI-based system developed to detect chili leaf diseases using Deep Learning.

## Models

- Custom CNN
- Vision Transformer (ViT)

## Dataset

The dataset contains 1,852 chili leaf images in 6 classes:

- Bacterial Spot
- Cercospora Leaf Spot
- Curl Virus
- Healthy Leaf
- Nutrition Deficiency
- White Spot

## Results

| Model | Accuracy | Epochs |
|---|---:|---:|
| Custom CNN | 69.69% | 20 |
| Vision Transformer (ViT) | 99.38% | 5 |

## Technologies

- Python
- TensorFlow / Keras
- PyTorch
- NumPy
- Pandas
- OpenCV
- Scikit-learn
- Matplotlib



## How to Run

### 1. Open the Project

Open the `ChiliDoc_Project` folder in VS Code.

### 2. Open Terminal

Open the VS Code terminal.

### 3. Create Virtual Environment

Run the following command:

    python -m venv venv

### 4. Activate Virtual Environment

For Windows PowerShell, run:

    venv\Scripts\activate

### 5. Install Required Libraries

    pip install -r requirements.txt

### 6. Run the Application

    python webapp\app.py

### 7. Open the Application

Open a web browser and visit:

    http://localhost:5000


## Trained Model

The trained Vision Transformer (ViT) model is located in:

    models/chilidoc_vit_model/

The application automatically loads the trained model from this folder.


## Important Notes

- The `venv` folder is not included in the project ZIP.
- Create the virtual environment using:

    python -m venv venv

- Install required packages using:

    pip install -r requirements.txt

- The trained ViT model is required for disease prediction.
- The dataset is not required to run the web application.
- Make sure the trained model is available inside:

    models/chilidoc_vit_model/

