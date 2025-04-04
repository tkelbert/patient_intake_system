import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import uuid
import os
from datetime import datetime

class PatientIntakeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Intake System")
        self.root.geometry("800x600")
        
        # Initialize patient data
        self.patients = self.load_patients()
        
        # Create main frames
        self.create_frames()
        self.create_form_widgets()
        self.create_patient_list()
        
    def create_frames(self):
        # Left frame for form
        self.form_frame = ttk.LabelFrame(self.root, text="Patient Information")
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Right frame for patient list
        self.list_frame = ttk.LabelFrame(self.root, text="Patient List")
        self.list_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
    def create_form_widgets(self):
        # Form labels and entries
        ttk.Label(self.form_frame, text="First Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.first_name_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.first_name_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(self.form_frame, text="Last Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.last_name_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.last_name_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(self.form_frame, text="Date of Birth (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.dob_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.dob_var).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(self.form_frame, text="Phone Number:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.phone_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.phone_var).grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(self.form_frame, text="Address:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.address_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.address_var).grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(self.form_frame, text="Reason for Visit:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.reason_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.reason_var).grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(self.form_frame, text="Notes:").grid(row=6, column=0, padx=5, pady=5, sticky="nw")
        self.notes_text = scrolledtext.ScrolledText(self.form_frame, width=30, height=5)
        self.notes_text.grid(row=6, column=1, padx=5, pady=5, sticky="ew")
        
        # Buttons
        button_frame = ttk.Frame(self.form_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add Patient", command=self.add_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights for form_frame
        self.form_frame.grid_columnconfigure(1, weight=1)
        
    def create_patient_list(self):
        # Create Treeview for patient list
        columns = ("ID", "First Name", "Last Name", "DOB", "Phone")
        self.patient_tree = ttk.Treeview(self.list_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.patient_tree.heading(col, text=col)
            self.patient_tree.column(col, width=80)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.patient_tree.yview)
        self.patient_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.patient_tree.pack(expand=True, fill=tk.BOTH)
        
        # Bind double-click event
        self.patient_tree.bind("<Double-1>", self.view_patient)
        
        # Load existing patients into the treeview
        self.update_patient_list()
        
    def load_patients(self):
        """Load patients from JSON file"""
        if os.path.exists("patients.json"):
            try:
                with open("patients.json", "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []
        else:
            return []
    
    def save_patients(self):
        """Save patients to JSON file"""
        with open("patients.json", "w") as file:
            json.dump(self.patients, file, indent=4)
    
    def update_patient_list(self):
        """Update the patient list display"""
        # Clear existing items
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)
        
        # Add patients to the treeview
        for patient in self.patients:
            self.patient_tree.insert("", tk.END, values=(
                patient["patient_id"],
                patient["first_name"],
                patient["last_name"],
                patient["date_of_birth"],
                patient["phone_number"]
            ))
    
    def validate_form(self):
        """Validate form input"""
        # Check required fields
        if not self.first_name_var.get().strip():
            messagebox.showerror("Error", "First Name is required.")
            return False
        
        if not self.last_name_var.get().strip():
            messagebox.showerror("Error", "Last Name is required.")
            return False
        
        dob = self.dob_var.get().strip()
        if not dob:
            messagebox.showerror("Error", "Date of Birth is required.")
            return False
        
        # Validate date format
        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Date of Birth must be in YYYY-MM-DD format.")
            return False
        
        if not self.phone_var.get().strip():
            messagebox.showerror("Error", "Phone Number is required.")
            return False
        
        return True
    
    def add_patient(self):
        """Add a new patient"""
        if not self.validate_form():
            return
        
        # Generate a 6-digit patient ID using UUID
        patient_id = str(uuid.uuid4().int)[:6]
        
        # Create new patient object
        patient = {
            "patient_id": patient_id,
            "first_name": self.first_name_var.get().strip(),
            "last_name": self.last_name_var.get().strip(),
            "date_of_birth": self.dob_var.get().strip(),
            "phone_number": self.phone_var.get().strip(),
            "address": self.address_var.get().strip(),
            "reason_for_visit": self.reason_var.get().strip(),
            "notes": self.notes_text.get("1.0", tk.END).strip()
        }
        
        # Add to patients list
        self.patients.append(patient)
        
        # Save to file
        self.save_patients()
        
        # Update patient list
        self.update_patient_list()
        
        # Clear form
        self.clear_form()
        
        messagebox.showinfo("Success", f"Patient added successfully with ID: {patient_id}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.dob_var.set("")
        self.phone_var.set("")
        self.address_var.set("")
        self.reason_var.set("")
        self.notes_text.delete("1.0", tk.END)
    
    def view_patient(self, event):
        """View details of selected patient"""
        # Get selected item
        selected_item = self.patient_tree.selection()
        if not selected_item:
            return
        
        # Get patient ID
        patient_id = self.patient_tree.item(selected_item[0], "values")[0]
        
        # Find patient in the list
        patient = next((p for p in self.patients if p["patient_id"] == patient_id), None)
        
        if patient:
            # Display patient details
            details = f"""
Patient ID: {patient["patient_id"]}
First Name: {patient["first_name"]}
Last Name: {patient["last_name"]}
Date of Birth: {patient["date_of_birth"]}
Phone Number: {patient["phone_number"]}
Address: {patient["address"]}
Reason for Visit: {patient["reason_for_visit"]}
Notes: {patient["notes"]}
            """
            messagebox.showinfo("Patient Details", details)

def main():
    root = tk.Tk()
    app = PatientIntakeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
