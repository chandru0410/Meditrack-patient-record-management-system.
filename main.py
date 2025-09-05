import logging
from meditrack import Patient,Doctor
from clinic_db import ClinicDB
from datetime import date

# Configure logging
logging.basicConfig(filename='meditrack.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Create DB instance
db = ClinicDB()

# Add sample patient
patient = Patient(id=1, name="Jayachandran", email="jayachandrankumar04@gmail.com",
                  phone="9876543210", age=22, gender="male")
db.add_patient(patient)

# Add sample doctor
doctor = Doctor(id=1, name="Dr. Flora", specialization="Dermatology")
db.add_doctor(doctor)

# Assign an appointment
db.assign_appointment(patient_id=1, doctor_id=1, date="2025-06-24")

# Record a prescription
db.record_prescription(patient_id=1, doctor_id=1, diagnosis="pigmentation", prescription="Vitamin C serum", date="2025-06-24")

# View patient history
history = db.get_patient_history(patient_id=1)

print("\n=== Patient History ===")
print(history)

# Add another patient
patient2 = Patient(id=2, name="Anjali Mehra", email="anjali.mehra@example.com",
                   phone="9876543211", age=28, gender="female")

db.add_patient(patient2)

doctor2 = Doctor(id=2, name="Dr. Chandru", specialization="Dermatology")
db.add_doctor(doctor2)


# Assign appointment and prescription for the new patient
db.assign_appointment(patient_id=2, doctor_id=2, date="2025-06-25")
db.record_prescription(patient_id=2, doctor_id=2, diagnosis="Acne", prescription="Benzoyl Peroxide", date="2025-06-25")

# Display patient 2 history
history2 = db.get_patient_history(patient_id=2)

print("\n=== Patient 2 History ===")
print(history2)

# Add another patient
patient3 = Patient(id=3, name="Girija", email="girija.04@example.com",
                   phone="9876543244", age=34, gender="female")

db.add_patient(patient3)

doctor3 = Doctor(id=3, name="Dr. senthil kumar", specialization="Dermatology")
db.add_doctor(doctor3)


# Assign appointment and prescription for the new patient
db.assign_appointment(patient_id=3, doctor_id=3, date="2025-06-30")
db.record_prescription(patient_id=3, doctor_id=3, diagnosis="open pores", prescription="Ninachinamide", date="2025-06-30")

# Display patient 2 history
history3 = db.get_patient_history(patient_id=3)

print("\n=== Patient 3 History ===")
print(history3)