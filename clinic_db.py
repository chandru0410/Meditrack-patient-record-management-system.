import sqlite3
import logging
from datetime import datetime
from meditrack import Patient, Doctor
from validation import is_valid_email, is_valid_phone

class ClinicDB:
    def __init__(self, db_name='clinic.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.create_tables()

    def __del__(self):
        self.conn.close()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            email TEXT UNIQUE,
                            phone TEXT UNIQUE,
                            age INTEGER,
                            gender TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            specialization TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            patient_id INTEGER,
                            doctor_id INTEGER,
                            date TEXT,
                            FOREIGN KEY (patient_id) REFERENCES patients(id),
                            FOREIGN KEY (doctor_id) REFERENCES doctors(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS prescriptions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            patient_id INTEGER,
                            doctor_id INTEGER,
                            diagnosis TEXT,
                            prescription TEXT,
                            date TEXT,
                            FOREIGN KEY (patient_id) REFERENCES patients(id),
                            FOREIGN KEY (doctor_id) REFERENCES doctors(id))''')

        self.conn.commit()

    def patient_exists(self, patient_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM patients WHERE id = ?", (patient_id,))
        return cursor.fetchone() is not None

    def doctor_exists(self, doctor_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM doctors WHERE id = ?", (doctor_id,))
        return cursor.fetchone() is not None

    def add_patient(self, patient: Patient):
        if not is_valid_email(patient.email) or not is_valid_phone(patient.phone):
            logging.warning("Invalid patient email or phone")
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO patients (name, email, phone, age, gender) VALUES (?, ?, ?, ?, ?)",
                           (patient.name, patient.email, patient.phone, patient.age, patient.gender))
            self.conn.commit()
            logging.info(f"Patient added: {patient.name}")
            return True
        except sqlite3.Error as e:
            logging.error(f"Error adding patient: {e}")
            return False

    def add_doctor(self, doctor: Doctor):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO doctors (name, specialization) VALUES (?, ?)",
                           (doctor.name, doctor.specialization))
            self.conn.commit()
            logging.info(f"Doctor added: {doctor.name}")
            return True
        except sqlite3.Error as e:
            logging.error(f"Error adding doctor: {e}")
            return False

    def assign_appointment(self, patient_id: int, doctor_id: int, date: str = None):
        if not self.patient_exists(patient_id) or not self.doctor_exists(doctor_id):
            logging.warning("Invalid patient or doctor ID")
            return False
        try:
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO appointments (patient_id, doctor_id, date) VALUES (?, ?, ?)",
                           (patient_id, doctor_id, date))
            self.conn.commit()
            logging.info(f"Appointment assigned: Patient {patient_id} → Doctor {doctor_id} on {date}")
            return True
        except sqlite3.Error as e:
            logging.error(f"Error assigning appointment: {e}")
            return False

    def record_prescription(self, patient_id: int, doctor_id: int, diagnosis: str, prescription: str, date: str = None):
        if not self.patient_exists(patient_id) or not self.doctor_exists(doctor_id):
            logging.warning("Invalid patient or doctor ID")
            return False
        try:
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO prescriptions (patient_id, doctor_id, diagnosis, prescription, date) VALUES (?, ?, ?, ?, ?)",
                           (patient_id, doctor_id, diagnosis, prescription, date))
            self.conn.commit()
            logging.info(f"Prescription recorded for Patient {patient_id}")
            return True
        except sqlite3.Error as e:
            logging.error(f"Error recording prescription: {e}")
            return False

    def get_patient_history(self, patient_id: int):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT a.date, d.name FROM appointments a
                          JOIN doctors d ON a.doctor_id = d.id
                          WHERE a.patient_id = ?''', (patient_id,))
        appointments = [{'date': row[0], 'doctor': row[1]} for row in cursor.fetchall()]

        cursor.execute('''SELECT p.date, d.name, p.diagnosis, p.prescription FROM prescriptions p
                          JOIN doctors d ON p.doctor_id = d.id
                          WHERE p.patient_id = ?''', (patient_id,))
        prescriptions = [{'date': row[0], 'doctor': row[1], 'diagnosis': row[2], 'prescription': row[3]} for row in cursor.fetchall()]

        return {'appointments': appointments, 'prescriptions': prescriptions}

    def get_patient(self, patient_id: int):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        return cursor.fetchone()

    def get_doctor(self, doctor_id: int):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
        return cursor.fetchone()
