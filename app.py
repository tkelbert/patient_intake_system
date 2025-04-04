from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)


@app.route('/')
def index():
    """Redirects the user from the root URL to the questionnaire form."""
    return redirect('/questionnaire')


@app.route('/questionnaire')
def questionnaire_form():
    """Displays the questionnaire form."""
    return render_template('questionnaire.html')


@app.route('/submit_questionnaire', methods=['POST'])
def submit_questionnaire():
    """Handles the submission of the questionnaire and writes to a JSON file."""
    patient_id = request.form['patient_id']
    feeling = request.form['feeling']
    symptoms = request.form['symptoms']
    notes = request.form['notes']

    questionnaire_data = {
        'patient_id': patient_id,
        'feeling': feeling,
        'symptoms': symptoms,
        'notes': notes
    }

    filename = f"patient_{patient_id}_questionnaire.json"
    try:
        with open(filename, 'w') as f:
            # Use indent for pretty formatting
            json.dump(questionnaire_data, f, indent=4)
        return f"Questionnaire submitted successfully! Data written to {filename}"
    except Exception as e:
        return f"An error occurred while writing to the file: {e}"


if __name__ == '__main__':
    app.run(debug=True)
