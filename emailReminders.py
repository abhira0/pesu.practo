import pandas as pd
import os
from termcolor import cprint

class Database:
    patients_database = {}
    def __init__(self):
        self.get_db()

    def get_db(self):
        tables_xlsx = os.listdir("./db")
        # for table_xlsx in tables_xlsx:
        patients = tables_xlsx[3].split(".")[0]
        self.patients_database[patients] = pd.read_excel(f"./db/{patients}")

db = Database()