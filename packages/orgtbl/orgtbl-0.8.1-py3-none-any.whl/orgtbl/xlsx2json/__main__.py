import json
import sys
import os
import pandas as pd
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font


xlsx_filename = None
xlsx_sheets = []


try:
    xlsx_filename = sys.argv[1]
except:
    print("Usage: PROGRAM <XLSX-FILE-TO-READ>")
    sys.exit(0)



with pd.ExcelFile(xlsx_filename) as f:
    xlsx_sheets = f.sheet_names

for sheet_name in xlsx_sheets:
    name_base = xlsx_filename + "." + sheet_name.lower()
    print("Sheet '%s' ..." % (sheet_name))
    df = pd.read_excel(xlsx_filename, dtype=str, header=None, sheet_name=sheet_name, keep_default_na=False)
    with open(name_base + ".cols.json", "w") as f:
        json_string = df.to_json()
        json_object = json.loads(json_string)
        json_string = json.dumps(json_object, indent=4)
        f.write(json_string)
    with open(name_base + ".rows.json", "w") as f:
        json_string = df.to_json(orient="records")
        json_object = json.loads(json_string)
        json_string = json.dumps(json_object, indent=4)
        f.write(json_string)
    # n_rows = len(df)
    # n_cols = len(df.columns)

# print(n_rows)
# print(n_cols)
# print(df.loc[0,0]) # A1
# print(df.loc[1,1])
