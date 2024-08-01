import sys
import os
import pandas as pd
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font


org_filename = None
xlsx_filename = None
sheet_names = [ "table%d" % x for x in range(1,100) ]

try:
    org_filename = sys.argv[1]
    xlsx_filename = sys.argv[2]
except:
    print("Usage: PROGRAM <ORG-FILE-TO-READ> <XLSX-FILE-TO-WRITE>")
    sys.exit(0)

try:
    sheet_names = sys.argv[3].split(" ")
except:
    pass

def single_table_values(data):
    lines = data.strip().split("\n")
    res = []
    for line in lines:
        cols = [ x.strip() for x in line.strip().split("|")[1:-1]]
        res.append(cols)
    return res

def extract_tables(filename):
    lines = []
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
    res = []

    lines_emptied_nontables = [ x if x.startswith("|") and x.endswith("|") else "" for x in lines ]
    data = "\n".join(lines_emptied_nontables)
    while "\n\n\n" in data:
        data = data.replace("\n\n\n", "\n\n")
    #lines = data.strip().split("\n")
    #print(lines)
    tables = data.strip().split("\n\n")
    for table_data in tables:
        res.append(single_table_values(table_data))
    return res

def string_xlsx(filename, tables, sheet_names):
    with pd.ExcelWriter(filename) as ew:
        for i in range(0, len(tables)):
            table = tables[i]
            sheet = sheet_names[i]

            df1 = pd.DataFrame(table)
            df1.to_excel(ew, sheet_name=sheet, index=False, header=False)
    
        # for col_idx in range(1,len(col_widths)+1):
        #     actual_width = col_widths[col_idx-1]
        #     column_letter = get_column_letter(col_idx)
        #     ew.sheets["Sheet_1"][column_letter + "1"].font = Font(bold=True)
        #     ew.sheets["Sheet_1"].column_dimensions[column_letter].width = actual_width


tables = extract_tables(filename=org_filename)
string_xlsx(filename=xlsx_filename, tables=tables, sheet_names=sheet_names)
