import os
import numpy as np
import pandas as pd
import urllib.request
import joblib
from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = settings.BASE_DIR
RECOMMANDATION_PATH = os.path.join(BASE_DIR, 'Data Science', 'Models', 'car_embeddings.pkl')
PREDICTION_PATH = os.path.join(BASE_DIR, 'Data Science', 'Models', 'Prediction.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, 'Data Science', 'Encoder', 'Prediction')
SCALER_PATH =  os.path.join(BASE_DIR, 'Data Science', 'Scaler', 'Prediction')
Data_Path = os.path.join(BASE_DIR, 'Data')
def load_data(filename):
    try:
        DATA_PATH = os.path.join(Data_Path, filename)
        data = pd.read_csv(DATA_PATH)
        return data
    except Exception as e:
        print(f'Data Load Error: {e}')
        return None

def save_data(data, filename):
    try:
        PATH = os.path.join(Data_Path, filename)
        data.to_csv(PATH, index=False)
    except Exception as e:
        print(f'Data Load Error: {e}')

def load_recommandation():
    try:
        if not os.path.exists(RECOMMANDATION_PATH):
            os.makedirs(os.path.dirname(RECOMMANDATION_PATH),exist_ok=True)
            url = "https://huggingface.co/abhaysinghsrinet/Car-Recommandation-Similarity-Matrix/resolve/main/car_embeddings.pkl"
            urllib.request.urlretrieve(url, RECOMMANDATION_PATH)
        car_embeddings = joblib.load(RECOMMANDATION_PATH)
        similarity_matrix = cosine_similarity(car_embeddings)
        return similarity_matrix
    except Exception as e:
        print(f"Recommendation Model Load Error: {e}")
        return None

def load_prediction():
    try:
        model = joblib.load(PREDICTION_PATH)
        return model
    except Exception as e:
        print(f'Prediction Model Load Error: {e}')
        return None

def load_encoder(col_name):
    try:
        file_name = f"{col_name}_Encoder.pkl"
        path = os.path.join(ENCODER_PATH, file_name)
        return joblib.load(path)
    except Exception as e:
        print(f"Encoder Error {col_name}: {e}")
        return None