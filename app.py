from flask import Flask, request, render_template, jsonify
import pandas as pd
from pycaret.time_series import *
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    print("Predict function called")
    # Get the file and the prediction period from the POST request
    f = request.files['datafile']
    predict_period = int(request.form['predict_period'])
    print(f"Received file: {f.filename}")
    print(f"Prediction period: {predict_period}")
    
    # Read the CSV file into a DataFrame
    # Assuming the CSV has a DateTime index and one column of values
    df = pd.read_csv(f, index_col=0, parse_dates=True, squeeze=True)
    
    # Initialize the setup
    s = setup(df, fh=predict_period, session_id=123, use_gpu=True, verbose=False, silent=True)

    # Compare models and select the best one
    best_model = compare_models()

    # Tune the best model
    tuned_model = tune_model(best_model)

    # Finalize the model and make predictions
    final_model = finalize_model(tuned_model)
    predictions = predict_model(final_model, fh=predict_period)

    # Prepare data for visualization
    original_data = df.reset_index().values.tolist()
    future_dates = predictions.index.tolist()
    prediction_values = predictions.values.tolist()
    future_data = [[str(date), value] for date, value in zip(future_dates, prediction_values)]

    data = {
        "original_data": original_data,
        "future_data": future_data,
    }
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
