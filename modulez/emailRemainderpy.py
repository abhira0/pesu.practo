import pandas as pd
import os
from termcolor import cprint
import re, datetime
from datetime import date
import smtplib, ssl


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


class reminder:
    db = Database()
    df = db.database["APPOINTMENT"]
    to_send = []
    today = date.today()
    schedule_date = str(today.day + 1) + "/" + str(today.month) + "/" + str(today.year)
    # print(df['PATIENT'][4])
    # print(schedule_date)
    # print(df['DATE'][5])
    # print(df['DATE'][5] == schedule_date)
    def validate(self):
        cprint("Patients having appointment:", "green")
        for i in range(len(self.df)):
            if self.df["DATE"][i] == self.schedule_date and self.df["REM"][i] == "Y":
                cprint("\t" + self.df["PATIENT"][i], "red")
                self.to_send.append(self.df["PATIENT"][i])

    def sendmail(self):
        self.validate()
        sender_email = "consultationspracto@gmail.com"
        port = 465
        password = "passwd@123"
        context = ssl.create_default_context()
        message = """\
            Subject: Appointment Remainder
            

            This is to remind you about your appointment today """
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, password)
            if self.to_send == []:
                cprint("No reminders to send", "red")
            else:
                for i in range(len(self.to_send)):
                    cprint("Sending reminder to" + "  -->  " + self.to_send[i], "red")
                    server.sendmail(sender_email, self.to_send[i], message)
                cprint("---All reminders sent :)", "red")


c = reminder()
c.sendmail()
