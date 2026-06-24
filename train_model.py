import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

if not os.path.exists('models'):
    os.makedirs('models')

# LOAD DATASET

df = pd.read_csv('dataset.csv')

X = df.drop('disease', axis=1)
y = df['disease']

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

model = RandomForestClassifier()
model.fit(X, y_encoded)

joblib.dump(model, './models/model.pkl')
joblib.dump(label_encoder, './models/label_encoder.pkl')

print("Model trained successfully")