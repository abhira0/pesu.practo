import pandas


class db:
    def get_db(self):
        ...

    def create_db(self):
        ...


class Patient:
    def __init__(self):
        ...

    def register(self):
        ...

    def login(self):
        ...

    def search(self):
        ...

    def book_appointments(self):
        ...

    def confirmation(self):
        ...


class Doctor:
    def __init__(self):
        ...

    def register(self):
        ...

    def fill_info(self):
        ...

    def patient_details(self):
        ...

    def patient_report(self):
        ...


class Admin:
    def __init__(self):
        ...

    def add_hospital(self):
        ...

    def add_doctor(self):
        ...

    def maintain_doctor_details(self):
        ...

    def maintain_patient_details(self):
        ...

    def cancel_doctors(self):
        ...


class Hospital:
    def __init__(self):
        ...

    def add_doctor(self):
        ...

    def add_fee(self):
        ...

    def view_patients(self):
        ...

    def notify_patients(self):
        ...

    def maintain_appointment_schedule(self):
        ...

    def maintain_details(self):
        ...
