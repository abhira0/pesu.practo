import pandas as pd
import os


class Database:
    database = {}

    def __init__(self):
        self.create_table()
        self.get_db()

    def get_db(self):
        tables_xlsx = os.listdir("./db")
        for table_xlsx in tables_xlsx:
            table_name = table_xlsx.split(".")[0]
            print(table_xlsx)
            self.database[table_name] = pd.read_excel(f"./db/{table_xlsx}")
            print(self.database[table_name])

    def create_table(self):
        DBT_USER = pd.DataFrame(
            columns=[
                "USER_ID",
                "FIRST_NAME",
                "LAST_NAME",
                "DOB",
                "ADDRESS",
                "EMAIL_ID",
                "PASSWORD",
                "GENDER",
                "AGE",
                "PHONE_NUMBER",
            ]
        )
        DBT_DOCTOR = pd.DataFrame(
            columns=[
                "DOCTOR_ID",
                "FIRST_NAME",
                "LAST_NAME",
                "ADDRESS",
                "SPECIALITY",
                "YOE",
                "WORKPLACE",
                "RATING",
                "EMAIL_ID",
                "PHONE_NUMBER",
                "AVAILABILITY",
            ]
        )
        DBT_ADMIN = pd.DataFrame(
            columns=[
                "ADMIN_NAME",
                "USER_ID",
                "DOCTOR_ID",
                "PASSWORD",
                "BOOKING_TIME",
                "TIMESTAMP",
                "HOSPITAL_NAME",
            ]
        )
        DBT_HOSPITAL = pd.DataFrame(
            columns=[
                "HOSPITAL_ID",
                "NAME",
                "ADDRESS",
                "EMAIL",
                "PHONE_NUMBER",
                "ZIP_CODE",
                "RATING",
            ]
        )

        db_tables = [i for i in locals() if i.startswith("DBT_")]
        for table_name in db_tables:
            if not os.path.exists(f"./db/{table_name}.xlsx"):
                temp_name = table_name.split("_")[1]
                print(f"CREATE TABLE {temp_name}")
                locals()[table_name].to_excel(f"./db/{table_name}.xlsx")


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


d = Database()