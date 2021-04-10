import pandas as pd
import os
from termcolor import cprint
import re, datetime


class utils:
    @staticmethod
    def checkIf(arr: list, text: str):
        for pattern in arr:
            if pattern.lower() == text.strip().lower():
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
                "EMAIL_ID",
                "SPECIALITY",
                "YOE",
                "RATING",
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
        DBT_HOSPITAL = pd.DataFrame(columns=["EMAIL", "PHONE_NUMBER", "LOCATION"])

        db_tables = [i for i in locals() if i.startswith("DBT_")]
        for table_name in db_tables:
            temp_name = table_name.split("_")[1]
            if not os.path.exists(f"./db/{temp_name}.xlsx"):
                print(f"CREATE TABLE {temp_name}")
                locals()[table_name].to_excel(f"./db/{temp_name}.xlsx", index=False)


db = Database()


class Patient:
    def __init__(self):
        self.__login_status = False

    def register(self, emailid=None):
        def get_ENTRY_EMAIL_ID():
            if emailid:
                return emailid
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
        if ENTRY_EMAIL_ID in db.database["PATIENT"]["EMAIL_ID"].values:
            cprint("[i] You already have an account. ", "cyan")
            if utils.checkIf(["yes", "y", "1"], input("Do you want to login? ")):
                self.login(emailid=ENTRY_EMAIL_ID)
                return "Redirected to Login Page"
            print("Bye")
            return "No Registration nor Login"
        # ----------------------------------------
        def get_ENTRY_PASSWORD():
            while True:
                tmp_inp = input("Enter the password: ")
                if len(tmp_inp) > 6:
                    return tmp_inp
                cprint("Length of the password must be greater than 6", "red")

        ENTRY_PASSWORD = get_ENTRY_PASSWORD()

        # ----------------------------------------
        def get_ENTRY_GENDER():
            while True:
                tmp_inp = input("Enter the gender (m/f): ")
                if tmp_inp.lower() in ["m", "male"]:
                    return "MALE"
                elif tmp_inp.lower() in ["f", "female"]:
                    return "FEMALE"
                cprint(
                    "[!] Please enter in proper format ['m','f','male','female']", "red"
                )

        ENTRY_GENDER = get_ENTRY_GENDER()

        # ----------------------------------------
        def get_ENTRY_AGE():
            while True:
                tmp_inp = input("Enter the age: ")
                try:
                    tmp_inp = int(tmp_inp)
                    if tmp_inp > 0:
                        return tmp_inp
                except:
                    ...
                cprint("[!] Please enter an integer > 0", "red")

        ENTRY_AGE = get_ENTRY_AGE()

        # ----------------------------------------
        def get_ENTRY_PHONE_NUMBER():
            while True:
                tmp_inp = input("Enter the phone number: ")
                if re.match("^\d{10}$", tmp_inp):
                    return tmp_inp.strip()
                cprint("[!] Please enter in the given format [\d\{10\}]", "red")

        ENTRY_PHONE_NUMBER = get_ENTRY_PHONE_NUMBER()
        db.database["PATIENT"].loc[len(db.database["PATIENT"])] = [
            j for i, j in locals().items() if i.startswith("ENTRY_")
        ]
        cprint("You have successfully registered into Practo.", "green")
        db.database["PATIENT"].to_excel("./db/PATIENT.xlsx", index=False)
        if utils.checkIf(["yes", "y", "1"], input("Do you want to login? ")):
            self.login(emailid=ENTRY_EMAIL_ID)
            return "Redirected to Login Page"

    def login(self, emailid=None):
        df = db.database["PATIENT"]

        def get_ENTRY_EMAIL_ID():
            if emailid:
                return emailid
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

        def get_ENTRY_PASSWORD():
            while True:
                tmp_inp = input("Enter the password: ")
                if tmp_inp != "":
                    return tmp_inp
                cprint("[!] Password cannot be empty", "red")

        ENTRY_EMAIL_ID = get_ENTRY_EMAIL_ID()
        # check if the patient wansnt registered
        if ENTRY_EMAIL_ID not in df["EMAIL_ID"].values:
            cprint("[i] You dont have an account. ", "cyan")
            if utils.checkIf(["yes", "y", "1"], input("Do you want to register? ")):
                self.register(emailid=ENTRY_EMAIL_ID)
                return "Redirected to Register Page"
            print("Bye")
            return "No Registration nor Login:"
        else:
            __utthara = df.loc[df["EMAIL_ID"] == ENTRY_EMAIL_ID].values[0][1]
            count = 3
            while count:
                tmp_inp = get_ENTRY_PASSWORD().strip()
                if tmp_inp == __utthara:
                    self.__login_status = True
                    cprint("Login Successful", "green")
                    return "Login Successful"
                count -= 1
                if count:
                    cprint(f"[!] Login Unsuccessful, tries allowed: {count}", "red")
        cprint("[i] Sorry, we couldn't log you in", "cyan")

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
    __usrs = {"admin": "admin", "root": "toor"}

    def __init__(self):
        self.__login_status = False
        __usr = input("Enter Admin Name: ")
        __pass = input("Enter Admin Password: ")
        try:
            if self.__usrs[__usr] == __pass:
                self.__login_status = True
                cprint("Login Successful", "green")
            else:
                self.__loginFalse("PASSWD")
                ...
        except:
            self.__loginFalse("USRNM")
            ...
        self.menu()

    def menu(self):
        if not self.__login_status:
            return

        print("-" * 19, "ADMIN", "-" * 20)
        try:
            tmp_inp = input(
                """Please enter your choice: [Ctrl+C to Quit]
                1. Add Doctor
                2. Add Hospital
                3. Print User DB
                4. Print Hospital DB
                5. Print Doctor DB\n"""
            )
        except:
            cprint("BYE BYE Admin avre", "magenta")
            exit(0)
        if tmp_inp == "1":
            self.add_doctor()
        elif tmp_inp == "2":
            self.add_hospital()
        elif tmp_inp == "3":
            self.print_table("PATIENT")
        elif tmp_inp == "4":
            self.print_table("HOSPITAL")
        elif tmp_inp == "5":
            self.print_table("DOCTOR")

    def __loginFalse(self, text):
        cprint(f"Login Unsuccessful: {text}", "red")
        del self

    def print_table(self, table_name):
        df = db.database[table_name]
        print(f"_____\n|\n{df}\n|\n`````")
        self.menu()

    def add_hospital(self):
        if not self.__login_status:
            # cprint("You have not logged in.", "red")
            return

        def get_ENTRY_EMAIL_ID():
            tmp_inp = input("Enter Hospital Email ID: ")
            while True:
                if tmp_inp == "":  # id must not be empty
                    cprint("[!] Email ID cannot be empty", "red")
                # id must be valid
                elif not re.match(r"[\w\d]+@[\d\w]+\.[\w]", tmp_inp):
                    cprint("[!] Email ID should be valid", "red")
                else:
                    break
                tmp_inp = input("Enter Hospital Email ID: ")
            return tmp_inp

        def get_ENTRY_PHONE_NUMBER():
            while True:
                tmp_inp = input("Enter Hospital the phone number: ")
                if re.match("^\d{10}$", tmp_inp):
                    return tmp_inp.strip()
                cprint("[!] Please enter in the given format [\d\{10\}]", "red")

        def get_ENTRY_LOCATION():
            while True:
                tmp_inp = input("Enter Hospital the location: ")
                if tmp_inp != "":
                    break
                cprint("[!] Location cannot be empty", "red")
            return tmp_inp

        df = db.database["HOSPITAL"]
        ENTRY_EMAIL_ID = get_ENTRY_EMAIL_ID()
        ENTRY_PHONE_NUMBER = get_ENTRY_PHONE_NUMBER()
        ENTRY_LOCATION = get_ENTRY_LOCATION()
        df.loc[len(df)] = [j for i, j in locals().items() if i.startswith("ENTRY_")]
        cprint("Entry for Hospital has been added.", "green")
        df.to_excel("./db/HOSPITAL.xlsx", index=False)
        self.menu()

    def add_doctor(self):
        if not self.__login_status:
            # cprint("You have not logged in.", "red")
            return

        def get_ENTRY_EMAIL_ID():
            tmp_inp = input("Enter Doctor's Email ID: ")
            while True:
                if tmp_inp == "":  # id must not be empty
                    cprint("[!] Email ID cannot be empty", "red")
                # id must be valid
                elif not re.match(r"[\w\d]+@[\d\w]+\.[\w]", tmp_inp):
                    cprint("[!] Email ID should be valid", "red")
                else:
                    break
                tmp_inp = input("Enter Doctor's Email ID: ")
            return tmp_inp

        def get_ENTRY_PHONE_NUMBER():
            while True:
                tmp_inp = input("Enter Doctor's phone number: ")
                if re.match("^\d{10}$", tmp_inp):
                    return tmp_inp.strip()
                cprint("[!] Please enter in the given format [\d\{10\}]", "red")

        def get_ENTRY_YOE():
            while True:
                tmp_inp = input("Enter Doctor's the Year of Experiance: ")
                try:
                    tmp_inp = int(tmp_inp)
                    if tmp_inp > 0:
                        return tmp_inp
                except:
                    ...
                cprint("[!] Please enter an integer > 0", "red")

        def get_ENTRY_RATING():
            while True:
                tmp_inp = input("Enter Doctor's the rating: ")
                try:
                    tmp_inp = float(tmp_inp)
                    if tmp_inp >= 0:
                        return tmp_inp
                except:
                    ...
                cprint("[!] Please enter an integer > 0", "red")

        def get_ENTRY_SPECIALITY():
            while True:
                tmp_inp = input("Enter the Doctor's Speciality [comma seperated]: ")
                if tmp_inp != "":
                    break
                cprint("[!] Speciality cannot be empty", "red")
            return [i.strip() for i in tmp_inp.split(",")]

        ENTRY_EMAIL_ID = get_ENTRY_EMAIL_ID()
        ENTRY_SPECIALITY = get_ENTRY_SPECIALITY()
        ENTRY_YOE = get_ENTRY_YOE()
        ENTRY_RATING = get_ENTRY_RATING()
        ENTRY_PHONE_NUMBER = get_ENTRY_PHONE_NUMBER()
        self.menu()

    def maintain_doctor_details(self):
        ...

    def maintain_patient_details(self):
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


class LogReg:
    def __init__(self):
        print("-" * 15, "LOGIN/REGISTER", "-" * 15)
        call_em = [self.patient, self.doctor, self.admin, self.hospital]
        ind = int(
            input(
                """Who are you?
              1. User
              2. Doctor
              3. Admin
              4. Hospital admin\n"""
            )
        )
        call_em[ind - 1]()

    def patient(self):
        temp_user = Patient()
        tmp_inp = input(
            """Please enter your choice:
            1. Register
            2. Login\n"""
        )
        if tmp_inp == "1":
            temp_user.register()
        elif tmp_inp == "2":
            temp_user.login()

    def admin(self):
        temp_user = Admin()

    def doctor(self):
        ...

    def hospital(self):
        ...


LogReg()