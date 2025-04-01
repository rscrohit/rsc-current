from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import os

app = Flask(__name__)

# Load and preprocess data
def load_data():
    data = pd.read_csv('data.csv')
    data['Grade of Concrete'] = 'M' + data['Grade of Concrete'].astype(str).str.strip()
    data['Grade Numeric'] = data['Grade of Concrete'].str.extract(r'(\d+)').astype(int)

    return data

data = load_data()
available_grades = [f'M{grade}' for grade in range(15, 75, 5)]  # M15 to M70 in steps of 5

# Train models
features = data[['Grade Numeric', 'Water-Cement Ratio (w/c)', 'Superplasticizer (%)',
                'Fly Ash (%)', 'GGBS (%)']]

targets = {
    'cement': data['Cement (kg)'],
    'fine': data['Fine Aggregate (kg)'],
    'coarse': data['Coarse Aggregate (kg)'],
    'water': data['Water in kg'],
    'strength': data['Compressive Strength (MPa)'],
    'tensile': data['Split Tensile Strength (MPa)'],
    'flexural': data['Flexural Strength (MPa)'],
    'absorption': data['Water Absorption (%)'],
    'cost': data['Cost (INR)'],
    'slump': data['Slump (mm)']
}

models = {}
for target_name, target_values in targets.items():
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(features, target_values)
    models[target_name] = model

@app.route('/')
def index():
    return render_template('index.html', grades=available_grades)

@app.route('/optimize', methods=['POST'])
def optimize():
    # Get form data
    grade = request.form.get('grade')
    grade_numeric = int(grade.replace('M', ''))
    wc_ratio = float(request.form.get('wcRatio'))
    superplasticizer = float(request.form.get('superplasticizer'))
    fly_ash = float(request.form.get('flyAsh'))
    ggbs = float(request.form.get('ggbs'))
    
    # Prepare input for prediction
    input_data = np.array([[grade_numeric, wc_ratio, superplasticizer, fly_ash, ggbs]])
    
    # Make predictions
    predictions = {}
    for target_name, model in models.items():
        predictions[target_name] = float(model.predict(input_data)[0])
    
    # Calculate sustainability score (lower is better)
    sustainability_score = (
        (predictions['cement'] * 0.9) +  # Cement has high CO2 emissions
        (predictions['water'] * 0.5) -   # Water consumption
        (fly_ash * 0.8) -                # Fly ash is a recycled material
        (ggbs * 0.7)                     # GGBS is a recycled material
    ) / 100
    
    # Normalize to 0-100 scale
    sustainability_score = max(0, min(100 - (sustainability_score * 10), 100))
    
    return jsonify({
        'cement': round(predictions['cement'], 2),
        'water': round(predictions['water'], 2),
        'fineAggregate': round(predictions['fine'], 2),
        'coarseAggregate': round(predictions['coarse'], 2),
        'compressiveStrength': round(predictions['strength'], 2),
        'tensileStrength': round(predictions['tensile'], 2),
        'flexuralStrength': round(predictions['flexural'], 2),
        'waterAbsorption': round(predictions['absorption'], 2),
        'cost': round(predictions['cost'], 2),
        'slump': round(predictions['slump'], 2),
        'sustainabilityScore': round(sustainability_score, 2)
    })

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)