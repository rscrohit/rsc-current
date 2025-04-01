Project Structure:

Flask_App/
├── app.py          # Main Flask application
├── data.csv        # Dataset file
├── templates/
│   └── index.html  # Frontend template
├── venv/           # Virtual environment
└── README.md       # Instructions file


# Instructions (README.md):

## Prerequisites
- Python 3.x installed
- pip installed

## Setting Up the Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate    # On Windows
```

## Installing Dependencies
```bash
pip install flask pandas scikit-learn numpy
```

## Running the Flask App
```bash
python app.py
```

## Access the Application
Open your browser and go to:
```
http://127.0.0.1:5000/
```

## Project Structure
- `app.py`: Main Flask application.
- `data.csv`: Dataset file used for model training and predictions.
- `templates/index.html`: Frontend template for user interaction.
- `venv/`: Virtual environment folder.
- `README.md`: Setup and usage instructions.

## Usage
The application predicts the optimal mix for concrete based on input parameters like grade, water-cement ratio, superplasticizer percentage, fly ash percentage, and GGBS percentage. The model outputs cement, water, fine aggregate, coarse aggregate, strength, tensile strength, flexural strength, water absorption, cost, slump, and a calculated sustainability score.

## Exiting the Environment
To deactivate the virtual environment, use:
```
deactivate
```
