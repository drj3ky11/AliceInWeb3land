import requests
import json

url = "https://graphql.bitquery.io"

payload = json.dumps({
   "query": "query ($network: EthereumNetwork!, $hash: String!) {\n  ethereum(network: $network) {\n    transactions(txHash: {is: $hash}) {\n      block {\n        height\n        timestamp {\n          time(format: \"%Y-%m-%d %H:%M:%S\")\n        }\n      }\n      amount\n      amount_usd: amount(in: USD)\n      currency {\n        symbol\n      }\n      creates {\n        address\n        annotation\n      }\n      error\n      success\n      sender {\n        address\n        annotation\n      }\n      to {\n        address\n        annotation\n      }\n      gas\n      gasPrice\n      gasCurrency {\n        symbol\n      }\n      gasValue\n      gas_value_usd: gasValue(in: USD)\n    }\n  }\n}\n",
   "variables": "{\n  \"limit\": 100,\n  \"offset\": 10,\n  \"network\": \"ethereum\",\n  \"hash\": \" \"\n}"
})
headers = {
   'Content-Type': 'application/json',
   'X-API-KEY': ' '
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
