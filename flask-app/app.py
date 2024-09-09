from flask import Flask, render_template, request
import boto3
import pandas as pd
import pickle
import os

app = Flask(__name__)

# S3 Config
S3_BUCKET = 'big-mart-sales-data'
MODEL_FILE = 'models/model.pkl'
LOCAL_MODEL_PATH = '/tmp/model.pkl'

# Function to download model from S3
def download_model():
    s3 = boto3.client('s3')
    s3.download_file(S3_BUCKET, MODEL_FILE, LOCAL_MODEL_PATH)
    with open(LOCAL_MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user input from form
        item_mrp = float(request.form['Item_MRP'])
        item_weight = float(request.form['Item_Weight'])
        outlet_year = int(request.form['Outlet_Establishment_Year'])

        # Load model and make predictions
        model = download_model()
        input_features = pd.DataFrame([[item_mrp, item_weight, outlet_year]], columns=['Item_MRP', 'Item_Weight', 'Outlet_Establishment_Year'])
        prediction = model.predict(input_features)[0]

        # Render result to webpage
        return render_template('index.html', prediction=prediction)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
