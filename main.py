import requests, json
from datetime import datetime
import pprint

response_txn = requests.get("https://api.etherscan.io/api?module=account&action=txlistinternal&address=0x722a131ef6961C3cb46d3667e0966d0AF431e60F&startblock=0&endblock=99999999&sort=asc&apikey=H5MAJ3SRA9ZN6UJXJG62JPHXG9YF9KF9ZB")
txns = json.loads(response_txn.text)

txn_filtered = []
sales_per_day = {}

for txn in txns["result"]:
    if txn["from"] == "0x7Be8076f4EA4A4AD08075C2508e481d6C946D12b".lower():
        if txn["isError"] == "0":
            date_complete = datetime.fromtimestamp(int(txn["timeStamp"]))
            date = date_complete.date()
            sales_per_day[str(date)] = 0
            response_price = requests.get("https://min-api.cryptocompare.com/data/v2/histoday?fsym=ETH&tsym=EUR&limit=1&toTs="+str(date_complete.timestamp()+86400)+"&api_key=b845ea0a472a48c64593408ed0566c50f311d98ec840d08204f6c62132ae611f")
            prices = json.loads(response_price.text)
            eth_eur = prices["Data"]["Data"][0]["low"]
            eth = float(txn["value"])*(10**-18)
            txn_filtered.append({"date": str(date_complete), "ETH": eth, "ETH/EUR": eth_eur, "EUR": eth*eth_eur})

with open("txn_filtered.txt", mode="w") as file:
    file.write(pprint.pformat(txn_filtered))

for txn in txn_filtered:
    sales_per_day[txn["date"].split(" ")[0]] += (round(txn["ETH"]*txn["ETH/EUR"], 2))

total = 0
for day in sales_per_day:
    if day.split("-")[0] == "2021":
        total += sales_per_day[day]

with open("sales.txt", mode="w") as file:
    file.write(pprint.pformat(sales_per_day))

print(total)
print(sales_per_day)
print(txn_filtered)

## 0xd5 etherscan = 268316.1, script = 244609.80091408754, DAPPRADAR = 249392,35 script EUR = 215024.21100499996
## corby script = 801575.3808652746, script EUR = 697327.0926970161

## manca solana, polygon


