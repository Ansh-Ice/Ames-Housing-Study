import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd

app = Flask(__name__)
model = pickle.load(open('regmodel.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

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

if __name__ == "__main__":
    app.run(debug=True)