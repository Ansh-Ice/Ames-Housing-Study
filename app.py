import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd

app = Flask(__name__)
# Advanced model
model = pickle.load(open('regmodel.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# Basic model
model_basic = pickle.load(open('basic_model.pkl', 'rb'))
scaler_basic = pickle.load(open('basic_scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # print("Data received for prediction:", data)
    # print(np.array(list(data.values())).reshape(1, -1))
    new_data = scaler.transform(np.array(list(data.values())).reshape(1, -1))
    # print("Scaled data:", new_data)
    output = model.predict(new_data)
    price = np.expm1(output)[0]
    print("Prediction output:", price)
    return {"predicted_price": price}

@app.route('/basic-form')
def basic_form():
    return render_template('basic_form.html')

@app.route('/basic-result')
def basic_result():
    return render_template('basic_result.html')

@app.route('/predict-basic', methods=['POST'])
def predict_basic():
    data = request.json
    # Extract and order the features correctly for the basic model
    feature_order = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 
                     'YearBuilt', 'FullBath', 'TotRmsAbvGrd', '1stFlrSF', 'GarageArea']
    
    # Create array in the correct feature order
    feature_values = np.array([data.get(feature, 0) for feature in feature_order]).reshape(1, -1)
    
    # Scale the data using basic scaler
    new_data_scaled = scaler_basic.transform(feature_values)
    
    # Make prediction
    output = model_basic.predict(new_data_scaled)
    price = np.expm1(output)[0]
    
    print("Basic Model Prediction output:", price)
    return {"predicted_price": price}   

if __name__ == "__main__":
    app.run(debug=True)