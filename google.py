import gspread

sa = gspread.service_account("service_account.json")
sh = sa.open("IT PARK")

wks = sh.worksheet("wks")

# print("Rows", wks.row_count)
# print("Cols", wks.col_count)

print(wks.acell('A9').value)
