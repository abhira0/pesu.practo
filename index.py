import sqlite3


class db:
    # con = sqlite3.connect("data.db")
    con = sqlite3.connect(":memory:")
    c = con.cursor()

    def createConnection(self):
        self.c.execute(
            """
        CREATE TABLE IF NOT EXISTS USER
        (   USER_ID int NOT NULL PRIMARY KEY AUTOINCREMENT,
            FIRST_NAME text NOT NULL,
            LAST_NAME text NOT NULL,
            DOB text NOT NULL,
            ADDRESS text NOT NULL,
            EMAIL_ID text NOT NULL,
            PASSWORD text NOT NULL,
            GENDER text,
            AGE int,
            PHONE_NUMBER int NOT NULL
        );
        """
        )
        self.c.execute(
            """
        CREATE TABLE IF NOT EXISTS DOCTOR
        (   USER_ID int NOT NULL PRIMARY KEY AUTOINCREMENT,
            FIRST_NAME text NOT NULL,
            LAST_NAME text NOT NULL,
            DOB text NOT NULL,
            ADDRESS text NOT NULL,
            EMAIL_ID text NOT NULL,
            PASSWORD text NOT NULL,
            GENDER text,
            AGE int,
            PHONE_NUMBER int NOT NULL
        );
        """
        )
        self.con.commit()


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
