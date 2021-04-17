import pandas as pd
import os
from termcolor import cprint
import re, datetime
from datetime import date
import smtplib, ssl

# class Database:
#     patients_database = {}
#     def __init__(self):
#         self.get_db()

#     def get_db(self):
#         tables_xlsx = os.listdir("./db")
#         patients = tables_xlsx[3].split(".")[0]
#         self.patients_database[patients] = pd.read_excel(f"./db/{patients}")

# db = Database()

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
df = db.database['APPOINTMENT']
to_send = []
today = date.today()
schedule_date =str(today.day+1)+'/'+str(today.month)+'/'+str(today.year)
for i  in range(len(df)):
    if(df['DATE'][i] == schedule_date and df['REM'][i] == 'Y'):
        print(df['PATIENT'][i])
        to_send.append(df['PATIENT'][i])

def sendmail(patients):

    sender_email = "consultationspracto@gmail.com"
    port = 465
    password = 'passwd@123'
    context = ssl.create_default_context()
    message = """\
        Subject: Appoinrment Remainder
        

        This is to remind you about your appointment today """
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        for i in range(len(patients)):
            print(patients[i])
            server.sendmail(sender_email, patients[i], message)

sendmail(['kushalkrishnappa333@gmial.com'])