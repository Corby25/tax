import web3
from openpyxl import load_workbook

with open("txns.txt") as file:
    list_hashes = file.readlines()

workbook_name = 'plusvalenze.xlsx'
wb = load_workbook(workbook_name)
page = wb.active

row_to_append = []
for hash in list_hashes:
    row_to_append.append()

new_companies = [['name3','address3','tel3','web3'], ['name4','address4','tel4','web4']]

for info in new_companies:
    page.append(info)

wb.save(filename=workbook_name)