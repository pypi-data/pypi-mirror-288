import sys
import os
import pandas as pd
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font


org_filename = None
xlsx_filename = None
sheet_names = [ "table%d" % x for x in range(1,100) ]
col_factor = 0.0


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

try:
    col_factor = float(sys.argv[4])
except:
    pass

def single_table_values(data):
    lines = data.strip().split("\n")
    res = []
    for line in lines:
        if len(line.replace("|", "").replace("-", "").replace("+", "").strip()) == 0:
            continue
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
    column_width_base = 1.2
    with pd.ExcelWriter(filename) as ew:
        for i in range(0, len(tables)):
            table = tables[i]
            sheet = sheet_names[i]
            n_col = len(table[0])

            df1 = pd.DataFrame(table)
            df1.to_excel(ew, sheet_name=sheet, index=False, header=False)
    
            if col_factor > 0.0:
                print("Determining column widths %s" % sheet)
                col_max = [0] * n_col
                col_max_actual = [0] * n_col
                for col_i in range(0, len(col_max)):
                    for row_i in range(0, len(table)):
                        cell_chars = len(table[row_i][col_i])
                        if cell_chars > col_max[col_i]:
                            col_max[col_i] = cell_chars
                            col_max_actual[col_i] = int(col_factor * col_max[col_i] * column_width_base)
                            # if col_max_actual[col_i] == 0:
                            #     col_max_actual[col_i] = column_width_base
                # print(col_max)
                # print(col_max_actual)
                print("Applying column widths %s" % sheet)
                for col_idx in range(1,len(col_max)+1):
                    actual_width = col_max_actual[col_idx-1]
                    column_letter = get_column_letter(col_idx)
                    #ew.sheets[sheet][column_letter + "1"].font = Font(bold=True)
                    ew.sheets[sheet].column_dimensions[column_letter].width = actual_width
                print("Applying column widths %s done" % sheet)

            else:
                print("Default column widths %s" % sheet)



tables = extract_tables(filename=org_filename)
string_xlsx(filename=xlsx_filename, tables=tables, sheet_names=sheet_names)
