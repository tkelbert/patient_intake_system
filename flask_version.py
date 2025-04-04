from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# Load patients data
def load_patients():
    """Load patients from JSON file"""
    if os.path.exists("patients.json"):
        try:
            with open("patients.json", "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    else:
        return []

# Save patients data
def save_patients(patients):
    """Save patients to JSON file"""
    with open("patients.json", "w") as file:
        json.dump(patients, file, indent=4)

@app.route('/')
def index():
    """Render the main page with patient list"""
    patients = load_patients()
    return render_template('index.html', patients=patients)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    """Add a new patient from form submission"""
    # Get form data
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    date_of_birth = request.form.get('date_of_birth', '').strip()
    phone_number = request.form.get('phone_number', '').strip()
    address = request.form.get('address', '').strip()
    reason_for_visit = request.form.get('reason_for_visit', '').strip()
    notes = request.form.get('notes', '').strip()
    
    # Validate required fields
    errors = []
    if not first_name:
        errors.append("First Name is required.")
    if not last_name:
        errors.append("Last Name is required.")
    if not date_of_birth:
        errors.append("Date of Birth is required.")
    else:
        # Validate date format
        try:
            datetime.strptime(date_of_birth, "%Y-%m-%d")
        except ValueError:
            errors.append("Date of Birth must be in YYYY-MM-DD format.")
    if not phone_number:
        errors.append("Phone Number is required.")
    
    if errors:
        return render_template('index.html', 
                               errors=errors,
                               first_name=first_name,
                               last_name=last_name,
                               date_of_birth=date_of_birth,
                               phone_number=phone_number,
                               address=address,
                               reason_for_visit=reason_for_visit,
                               notes=notes,
                               patients=load_patients())
    
    # Generate a 6-digit patient ID using UUID
    patient_id = str(uuid.uuid4().int)[:6]
    
    # Create new patient object
    patient = {
        "patient_id": patient_id,
        "first_name": first_name,
        "last_name": last_name,
        "date_of_birth": date_of_birth,
        "phone_number": phone_number,
        "address": address,
        "reason_for_visit": reason_for_visit,
        "notes": notes
    }
    
    # Add to patients list
    patients = load_patients()
    patients.append(patient)
    
    # Save to file
    save_patients(patients)
    
    # Redirect to home page
    return redirect(url_for('index'))

@app.route('/api/patient/<patient_id>')
def get_patient(patient_id):
    """API endpoint to get patient details by ID"""
    patients = load_patients()
    patient = next((p for p in patients if p["patient_id"] == patient_id), None)
    
    if patient:
        return jsonify(patient)
    else:
        return jsonify({"error": "Patient not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
