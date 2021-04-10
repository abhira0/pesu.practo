import pandas as pd
import os
from termcolor import cprint
import re, datetime


class utils:
    @staticmethod
    def checkIf(arr: list, text: str):
        for pattern in arr:
            if pattern.to_lower() == text.strip().to_lower():
                return True
        return False

    @staticmethod
    def isValidDate(date: str):
        d, m, y = map(int, date)
        try:
            datetime.datetime(d, m, y)
        except:
            return False
        return True


class Database:
    database = {}

    def __init__(self):
        self.create_table()
        self.get_db()

    def get_db(self):
        tables_xlsx = os.listdir("./db")
        for table_xlsx in tables_xlsx:
            table_name = table_xlsx.split(".")[0]
            self.database[table_name] = pd.read_excel(f"./db/{table_xlsx}")

    def create_table(self):
        DBT_PATIENT = pd.DataFrame(
            columns=["EMAIL_ID", "PASSWORD", "GENDER", "AGE", "PHONE_NUMBER"]
        )
        DBT_DOCTOR = pd.DataFrame(
            columns=[
                "SPECIALITY",
                "YOE",
                "RATING",
                "EMAIL_ID",
                "PHONE_NUMBER",
                "AVAILABILITY",
            ]
        )
        DBT_ADMIN = pd.DataFrame(
            columns=[
                "ADMIN_NAME",
                "PID",
                "DID",
                "PASSWORD",
                "BOOKING_TIME",
                "TIMESTAMP",
                "HOSPITAL_NAME",
            ]
        )
        DBT_HOSPITAL = pd.DataFrame(columns=["HOSPITAL_ID", "EMAIL", "PHONE_NUMBER"])

        db_tables = [i for i in locals() if i.startswith("DBT_")]
        for table_name in db_tables:
            temp_name = table_name.split("_")[1]
            if not os.path.exists(f"./db/{temp_name}.xlsx"):
                print(f"CREATE TABLE {temp_name}")
                locals()[table_name].to_excel(f"./db/{temp_name}.xlsx")


db = Database()


class Patient:
    __login_status = False

    def __init__(self):
        ...

    def register(self):
        def get_ENTRY_EMAIL_ID():
            tmp_inp = input("Enter Your Email ID: ")
            while True:
                if tmp_inp == "":  # id must not be empty
                    cprint("[!] Email ID cannot be empty", "red")
                # id must be valid
                elif not re.match(r"[\w\d]+@[\d\w]+\.[\w]", tmp_inp):
                    cprint("[!] Email ID should be valid", "red")
                else:
                    break
                tmp_inp = input("Enter Your Email ID: ")
            return tmp_inp

        ENTRY_EMAIL_ID = get_ENTRY_EMAIL_ID()
        # check if the patient had already registered
        if ENTRY_EMAIL_ID in db.database["PATIENT"]["EMAIL_ID"]:
            cprint("[i] You already have an account. ", "cyan")
            if utils.checkIn(["yes", "y", "1"], input("Do you want to login? ")):
                self.login()
                return "Redirected to Login Page"
            print("Bye")
            return "No Registration nor Login"
        # ----------------------------------------
        def get_ENTRY_PASSWORD():
            tmp_inp = input("Enter the password: ")
            while True:
                if len(tmp_inp) < 6:
                    cprint("Length of the password must be greater than 4", "red")
                tmp_inp = input("Enter the password: ")
            return tmp_inp

        ENTRY_PASSWORD = get_ENTRY_PASSWORD()

        # ----------------------------------------
        def get_ENTRY_GENDER():
            tmp_inp = input("Enter the gender (m/f): ")
            while True:
                if tmp_inp.to_lower() in ["m", "f", "male", "female"]:
                    cprint(
                        "Please enter in proper format ['m','f','male','female']", "red"
                    )
                tmp_inp = input("Enter the gender (m/f): ")
            return tmp_inp

        ENTRY_PASSWORD = get_ENTRY_PASSWORD()

        # ENTRY_GENDER = input("Enter Your : ")
        # ENTRY_AGE = input("Enter Your : ")
        # ENTRY_PHONE_NUMBER = input("Enter Your : ")

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


temp_user = Patient()
temp_user.register()