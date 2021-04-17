from termcolor import cprint
import re, datetime, random
from modulez.dbpy import *


class utils:
    @staticmethod
    def checkIf(arr: list, text: str):
        # checks whether the given pattern matches the given text by ignoring cases (force all to lower case)
        for pattern in arr:
            if pattern.lower() == text.strip().lower():
                return True
        return False

    @staticmethod
    def isValidDate(date: str):
        # date must be in the format dd/mm/yyyy
        try:
            date = [i.strip() for i in date.split("/")]
            d, m, y = map(int, date)
            # parameter for datetime.datetime() is in the order year, month, day ...
            # if datetime.date.today() <= datetime.datetime(y, m, d):
            return True
        except:
            ...
        return False


db = Database()


class Patient:
    def __init__(self):
        self.__login_status = False
        tmp_inp = input(
            """>> Please enter your choice:
            1. Register
            2. Login\n"""
        )
        if tmp_inp == "1":
            self.register()
        elif tmp_inp == "2":
            self.login()
        if self.__login_status:
            self.menu

    def register(self, emailid=None):
        def get_ENTRY_EMAIL_ID():
            if emailid:
                return emailid
            tmp_inp = input("> Enter Your Email ID: ")
            while True:
                if tmp_inp == "":  # id must not be empty
                    cprint("[!] Email ID cannot be empty", "red")
                # id must be valid
                elif not re.match(r"[\w\d]+@[\d\w]+\.[\w]", tmp_inp):
                    cprint("[!] Email ID should be valid", "red")
                else:
                    break
                tmp_inp = input("> Enter Your Email ID: ")
            return tmp_inp

        ENTRY_EMAIL_ID = get_ENTRY_EMAIL_ID()
        # check if the patient had already registered
        if ENTRY_EMAIL_ID in db.database["PATIENT"]["EMAIL_ID"].values:
            cprint("[i] You already have an account. ", "cyan")
            if utils.checkIf(["yes", "y", "1"], input("> Do you want to login? ")):
                self.login(emailid=ENTRY_EMAIL_ID)
                return "Redirected to Login Page"
            print("Bye")
            return "No Registration nor Login"
        # ----------------------------------------
        def get_ENTRY_PASSWORD():
            while True:
                tmp_inp = input("> Enter the password: ")
                if len(tmp_inp) > 6:
                    return tmp_inp
                cprint("Length of the password must be greater than 6", "red")

        ENTRY_PASSWORD = get_ENTRY_PASSWORD()

        # ----------------------------------------
        def get_ENTRY_GENDER():
            while True:
                tmp_inp = input("> Enter the gender (m/f): ")
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
                tmp_inp = input("> Enter the age: ")
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
                tmp_inp = input("> Enter the phone number: ")
                if re.match("^\d{10}$", tmp_inp):
                    return tmp_inp.strip()
                cprint("[!] Please enter in the given format [\d\{10\}]", "red")

        ENTRY_PHONE_NUMBER = get_ENTRY_PHONE_NUMBER()
        db.database["PATIENT"].loc[len(db.database["PATIENT"])] = [
            j for i, j in locals().items() if i.startswith("ENTRY_")
        ]
        cprint("You have successfully registered into Practo.", "green")
        db.database["PATIENT"].to_excel("./db/PATIENT.xlsx", index=False)
        if utils.checkIf(["yes", "y", "1"], input("> Do you want to login? ")):
            self.login(emailid=ENTRY_EMAIL_ID)
            return "Redirected to Login Page"

    def login(self, emailid=None):
        df = db.database["PATIENT"]

        def get_ENTRY_EMAIL_ID():
            if emailid:
                return emailid
            tmp_inp = input("> Enter Your Email ID: ")
            while True:
                if tmp_inp == "":  # id must not be empty
                    cprint("[!] Email ID cannot be empty", "red")
                # id must be valid
                elif not re.match(r"[\w\d]+@[\d\w]+\.[\w]", tmp_inp):
                    cprint("[!] Email ID should be valid", "red")
                else:
                    break
                tmp_inp = input("> Enter Your Email ID: ")
            return tmp_inp

        def get_ENTRY_PASSWORD():
            while True:
                tmp_inp = input("> Enter the password: ")
                if tmp_inp != "":
                    return tmp_inp
                cprint("[!] Password cannot be empty", "red")

        ENTRY_EMAIL_ID = get_ENTRY_EMAIL_ID()
        # check if the patient wansnt registered
        if ENTRY_EMAIL_ID not in df["EMAIL_ID"].values:
            cprint("[i] You dont have an account. ", "cyan")
            if utils.checkIf(["yes", "y", "1"], input("> Do you want to register? ")):
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
                    self.emailid = ENTRY_EMAIL_ID
                    cprint("Login Successful", "green")
                    self.menu()
                    return "Login Successful"
                count -= 1
                if count:
                    cprint(f"[!] Login Unsuccessful, tries allowed: {count}", "red")
        cprint("[i] Sorry, we couldn't log you in", "cyan")

    def menu(self):
        if not self.__login_status:
            return

        print("-" * 20, "USER", "-" * 20)
        try:
            tmp_inp = input(
                """>> Please enter your choice: [Ctrl+C to Quit]
                1. Book Appointment
                2. Cancel Appointment\n"""
            )
        except:
            cprint("Bella ciao", "magenta")
            exit(0)
        if tmp_inp == "1":
            self.book_appointments()
        if tmp_inp == "2":
            self.delete_appointment()

    def get_specialization(self, search_text):
        if re.findall(r"(fever)|(cough)|(cold)|(headache)|(bodypain)", search_text):
            return "General"
        if re.findall(r"(heart)", search_text):
            return "Cardiologist"
        if re.findall(r"(rashes)|(acne)|(pimple)|(skin)", search_text):
            return "Dermatologist"
        if re.findall(r"(fracture)", search_text):
            return "Surgeon"
        return "General"

    def book_appointments(self):
        if not self.__login_status:
            return

        def get_search_text():
            while True:
                tmp = input(">> Enter the problem: ")
                if tmp:
                    return tmp
                cprint("[!] Problem cannot be empty", "red")

        def get_ENTRY_SLOT():
            while True:
                tmp = input("> Any one in 1,2,3,4,5: ")
                try:
                    x = int(tmp)
                    if x in [1, 2, 3, 4, 5]:
                        return x
                except:
                    ...
                cprint("[!] Enter an integer from the given set", "red")

        def get_ENTRY_DATE():
            while True:
                tmp = input("> Enter the date [dd/mm/yyyy]: ")
                if utils.isValidDate(tmp):
                    return tmp
                cprint("[!] Please enter a valid date", "red")

        def get_ENTRY_REM():
            tmp = input("Do you wanna get remainded? [yes|y|1]: ")
            if utils.checkIf(["yes", "y", "1"], tmp):
                return "Y"
            else:
                return "N"

        search_text = get_search_text()
        spec_req = self.get_specialization(search_text)
        df = db.database["DOCTOR"]
        doctors = {i[1][0]: i[0] for i in df.iterrows() if spec_req in i[1][1]}
        print(">> Please select the doctor: ")
        for count, doctor_name in enumerate(doctors):
            print(f"\t\t{count+1}. {doctor_name}")
        ind = int(input("> Number? : "))
        ENTRY_DOCTOR = list(doctors.keys())[ind - 1]
        ENTRY_PATIENT = self.emailid
        df = db.database["APPOINTMENT"]
        for _ in range(5):
            ENTRY_DATE = get_ENTRY_DATE()
            ENTRY_SLOT = get_ENTRY_SLOT()
            temp_series = (df["DATE"] == ENTRY_DATE) & (df["SLOT"] == ENTRY_SLOT)
            #
            if not df.loc[(df["DOCTOR"] == ENTRY_DOCTOR) & temp_series].empty:
                txt = "[i] We are sorry to say that the timeslot has already been booked\nPlease select another slot"
                cprint(txt, "cyan")
                continue
            if not df.loc[(df["PATIENT"] == ENTRY_PATIENT) & temp_series].empty:
                txt = "[i] You have been already appointed for this timeslot\nPlease select another slot"
                cprint(txt, "cyan")
            else:
                break
        ENTRY_REM = get_ENTRY_REM()
        df = db.database["APPOINTMENT"]
        df.loc[len(df)] = [j for i, j in locals().items() if i.startswith("ENTRY_")]
        cprint("Entry for Appointment has been added.", "green")
        df.to_excel("./db/APPOINTMENT.xlsx", index=False)
        self.menu()

    def delete_appointment(self):
        def get_index():
            while True:
                try:
                    ind = int(input("Enter the index: "))
                    if ind in range(0, len(aptmnts)):
                        return ind
                except:
                    ...
                cprint("[!] Enter the valid index", "red")

        df = db.database["APPOINTMENT"]
        aptmnts = [i[1] for i in df.iterrows() if self.emailid in i[1][1]]
        aptinds = [i[0] for i in df.iterrows() if self.emailid in i[1][1]]
        slot_time_map = {
            1: "8-10 AM",
            2: "10 AM-12 PM",
            3: "1-3 PM",
            4: "3-5 PM",
            5: "6-8 PM",
        }
        if aptmnts:
            print(">> Enter the index of the doctor: ")
            for count, i in enumerate(aptmnts):
                print(
                    f"\t{count+1}. Doctor: {i[0]}, Date: {i[2]}, Time Slot: {i[3]}, Time: {slot_time_map[i[3]]}"
                )
            ind = get_index()
            entry_to_delete = aptmnts[ind - 1]
            cprint(
                f"Deleting the entry: Doctor: {i[0]}, Date: {i[2]}, Time Slot: {i[3]}, Time: {slot_time_map[i[3]]}",
                "red",
            )
            df.drop(df.index[[aptinds[ind - 1]]], inplace=True)
            df.to_excel("./db/APPOINTMENT.xlsx", index=False)
        else:
            cprint("Sorry to say that you have not booked any appointment", "red")
        self.menu()


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
        __usr = input("> Enter Admin Name: ")
        __pass = input("> Enter Admin Password: ")
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
                """>> Please enter your choice: [Ctrl+C to Quit]
                1. Add Doctor
                2. Print User DB
                3. Print Doctor DB\n"""
            )
        except:
            cprint("BYE BYE Admin avre", "magenta")
            exit(0)
        if tmp_inp == "1":
            self.add_doctor()
        elif tmp_inp == "2":
            self.print_table("PATIENT")
        elif tmp_inp == "3":
            self.print_table("DOCTOR")

    def __loginFalse(self, text):
        cprint(f"Login Unsuccessful: {text}", "red")
        del self

    def print_table(self, table_name):
        if not self.__login_status:
            # cprint("You have not logged in.", "red")
            return
        df = db.database[table_name]
        print(f"_____\n|\n{df}\n|\n`````")
        self.menu()

    def add_doctor(self):
        if not self.__login_status:
            # cprint("You have not logged in.", "red")
            return

        def get_ENTRY_EMAIL_ID():
            tmp_inp = input("> Enter Doctor's Email ID: ")
            while True:
                if tmp_inp == "":  # id must not be empty
                    cprint("[!] Email ID cannot be empty", "red")
                # id must be valid
                elif not re.match(r"[\w\d]+@[\d\w]+\.[\w]", tmp_inp):
                    cprint("[!] Email ID should be valid", "red")
                else:
                    break
                tmp_inp = input("> Enter Doctor's Email ID: ")
            return tmp_inp

        def get_ENTRY_PHONE_NUMBER():
            while True:
                tmp_inp = input("> Enter Doctor's phone number: ")
                if re.match("^\d{10}$", tmp_inp):
                    return tmp_inp.strip()
                cprint("[!] Please enter in the given format [\d\{10\}]", "red")

        def get_ENTRY_YOE():
            while True:
                tmp_inp = input("> Enter Doctor's the Year of Experiance: ")
                try:
                    tmp_inp = int(tmp_inp)
                    if tmp_inp > 0:
                        return tmp_inp
                except:
                    ...
                cprint("[!] Please enter an integer > 0", "red")

        def get_ENTRY_RATING():
            while True:
                tmp_inp = input("> Enter Doctor's the rating: ")
                try:
                    tmp_inp = float(tmp_inp)
                    if tmp_inp >= 0:
                        return tmp_inp
                except:
                    ...
                cprint("[!] Please enter an float > 0", "red")

        def get_ENTRY_SPECIALITY():
            while True:
                tmp_inp = input("> Enter the Doctor's Speciality [comma seperated]: ")
                if tmp_inp != "":
                    break
                cprint("[!] Speciality cannot be empty", "red")
            return [i.strip() for i in tmp_inp.split(",")]

        ENTRY_EMAIL_ID = get_ENTRY_EMAIL_ID()
        ENTRY_SPECIALITY = get_ENTRY_SPECIALITY()
        ENTRY_YOE = get_ENTRY_YOE()
        ENTRY_RATING = get_ENTRY_RATING()
        ENTRY_PHONE_NUMBER = get_ENTRY_PHONE_NUMBER()
        ENTRY_AVAILABILITY = "N"

        df = db.database["DOCTOR"]
        df.loc[len(df)] = [j for i, j in locals().items() if i.startswith("ENTRY_")]
        cprint("Entry for Doctor has been added.", "green")
        df.to_excel("./db/DOCTOR.xlsx", index=False)
        self.menu()

    def maintain_doctor_details(self):
        ...

    def maintain_patient_details(self):
        ...


class LogReg:
    def __init__(self):
        print("-" * 15, "LOGIN/REGISTER", "-" * 15)
        call_em = [self.patient, self.doctor, self.admin]
        ind = int(
            input(
                """>> Who are you?
              1. User
              2. Doctor
              3. Admin\n"""
            )
        )
        call_em[ind - 1]()

    def patient(self):
        temp_user = Patient()

    def admin(self):
        temp_user = Admin()

    def doctor(self):
        ...


LogReg()
