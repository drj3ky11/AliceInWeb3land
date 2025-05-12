import requests
import json

url = "https://graphql.bitquery.io"

payload = json.dumps({
   "query": "query ($network: EthereumNetwork!, $hash: String!, $limit: Int!, $offset: Int!) {\n  ethereum(network: $network) {\n    smartContractEvents(\n      options: {limit: $limit, offset: $offset}\n      txHash: {is: $hash}\n    ) {\n      smartContract {\n        address {\n          address\n          annotation\n        }\n        contractType\n        protocolType\n      }\n      smartContractEvent {\n        name\n        signatureHash\n      }\n      count\n    }\n  }\n}\n",
   "variables": "{\n  \"limit\": 10,\n  \"offset\": 0,\n  \"network\": \"ethereum\",\n  \"hash\": \" \"\n}"
})
headers = {
   'Content-Type': 'application/json',
   'X-API-KEY': ' '
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
