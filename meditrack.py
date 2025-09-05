# Data Classes

#class patient
class Patient:      
    def __init__(self, id, name, email, phone, age, gender):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.age = age
        self.gender = gender

    def display(self):
        print("patient Details:")
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"email: {self.email}")
        print(f"phone: {self.phone}")
        print(f"age: {self.age}")
        print(f"gender: {self.gender}")
        print()

#class patient
class Doctor:       
    def __init__(self, id, name, specialization):
        self.id = id
        self.name = name
        self.specialization = specialization

    def display_2(self):
        print("Doctor Details:")
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Specialization: {self.specialization}")
        print()


# Correct usage
patient_obj = Patient(id=1, name="k jayachandran", email="jayachandrankumar04@gmail.com", phone=95660330, age=22, gender="male")
doctor_obj = Doctor(id=101, name="Dr. Defodil", specialization="Dermatology")

patient_obj.display()
doctor_obj.display_2()


