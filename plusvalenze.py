from web3 import Web3, EthereumTesterProvider
from openpyxl import load_workbook
from datetime import datetime
import requests, json

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/6b46939a901e4fb798dc0aa82ce92781'))
w3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/6b46939a901e4fb798dc0aa82ce92781'))
print(w3.isConnected())

with open("txns.txt") as file:
    list_hashes = file.readlines()

workbook_name = 'plusvalenze.xlsx'
wb = load_workbook(workbook_name)
page = wb.active

row_to_append = []

for hash in list_hashes:
    txn = w3.eth.getTransaction(hash.strip())
    timestamp = dict(w3.eth.get_block(txn.blockNumber))["timestamp"]

    response_price = requests.get(
        "https://min-api.cryptocompare.com/data/v2/histoday?fsym=ETH&tsym=EUR&limit=1&toTs=" + str(
            timestamp + 86400) + "&api_key=b845ea0a472a48c64593408ed0566c50f311d98ec840d08204f6c62132ae611f")
    prices = json.loads(response_price.text)
    eth_eur = prices["Data"]["Data"][1]["low"]

    row_to_append.append([txn.hash, datetime.fromtimestamp(timestamp), eth_eur, "", w3.fromWei(int(txn.value), 'ether')])

for row in row_to_append:
    page.append(row)

wb.save(filename=workbook_name)