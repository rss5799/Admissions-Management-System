import logging
import pandas as pd
from pathlib import Path

CSV_PATH = Path("DummyDataComplete.csv")

class StudentCSVHandler:
    def __init__(self, filepath: Path = CSV_PATH):
        self.filepath = filepath
        self.df = pd.read_csv(self.filepath)
        self.df["id"] = self.df["id"].astype(str).str.strip()

    def refresh(self):
        self.df = pd.read_csv(self.filepath)
        self.df["id"] = self.df["id"].astype(str).str.strip()

    def get_student_by_id(self, student_id):
        self.refresh()
        student_id = str(student_id).strip()
        record = self.df[self.df["id"] == student_id]
        return None if record.empty else record.iloc[0].to_dict()

    def update_student_fields(self, student_id, updates):
        self.refresh()
        student_id = str(student_id).strip()
        index = self.df[self.df["id"] == student_id].index
        if index.empty:
            raise ValueError(f'Student ID {student_id} not found.')

        for column, value in updates.items():
            self.df.loc[index, column] = value

        self.df.to_csv(self.filepath, index=False)


'''
logging.basicConfig(
    filename="outt.txt",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    )
logging.info(f"Student ID: [student_id]")
CSV_PATH = Path(__file__).resolve().parent.parent.parent / "DummyDataComplete.csv"

student_df = pd.read_csv('DummyDataComplete.csv')


def update_student_fields(student_id, updates, filepath: Path = CSV_PATH):
    df = pd.read_csv(filepath)

    index = df[df["id"] == student_id].index

    if index.empty:
        raise ValueError(f'Student ID {student_id} not found.')
    
    for column, value in updates.items():
        df.loc[index, column] = value

    df.to_csv(filepath, index=False)



def get_student_by_id(student_id, filepath: Path = CSV_PATH):
    logging.info("Raw student_id from request/session:", repr(student_id))

    df = pd.read_csv(filepath)

    logging.info("Raw IDs from CSV:")

    for idx, row in df.iterrows():
        row_id = row["id"]
        logging.info(f"- {repr(row_id)} == (repr(student_id)) ? -> {row_id == student_id}")
              
    #record = df[df["id"] == student_id]
    record = df[df["id"].astype(str).str.strip() == str(student_id).strip()]

    if record.empty:
        logging.info(" No match found using direct comparison")
        return None

    logging.info(" Match found!!!")
    return record.iloc[0].to_dict()


def normalize_id(id_value):
    return str(id_value).strip()



def get_student_by_id(student_id, filepath: Path = CSV_PATH):
    
    #Gets student record by id as a dict
    
    df = pd.read_csv(filepath)
    record = df[df["id"] == student_id]
    if record.empty:
        return None
        return record.iloc[0].to_dict()
'''
