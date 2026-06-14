from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

application = Flask(__name__)
app = application

ridge_model = pickle.load(open("models/ridge.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predictdata", methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'POST':
        temperature = float(request.form.get('Temperature'))
        Rh = float(request.form.get('RH'))
        Ws = float(request.form.get('Ws'))
        Rain = float(request.form.get('Rain'))
        Ffmc = float(request.form.get('FFMC'))
        Dmc = float(request.form.get('DMC'))
        Isi = float(request.form.get('ISI'))
        Classes = float(request.form.get('Classes'))
        Region = float(request.form.get('Region'))

        new_data = scaler.transform([[temperature, Rh, Ws, Rain, Ffmc, Dmc, Isi, Classes, Region]])
        result = ridge_model.predict(new_data)
        print(new_data)
        print(result)

        return render_template("home.html", results = result[0])
    else:
        return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
