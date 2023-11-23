import requests
import json

url = "https://graphql.bitquery.io"

payload = json.dumps({
   "query": "query ($network: EthereumNetwork!, $hash: String!, $limit: Int!, $offset: Int!) {\n  ethereum(network: $network) {\n    smartContractEvents(\n      options: {limit: $limit, offset: $offset}\n      txHash: {is: $hash}\n    ) {\n      smartContract {\n        address {\n          address\n          annotation\n        }\n        contractType\n        protocolType\n      }\n      smartContractEvent {\n        name\n        signatureHash\n      }\n      count\n    }\n  }\n}\n",
   "variables": "{\n  \"limit\": 10,\n  \"offset\": 0,\n  \"network\": \"ethereum\",\n  \"hash\": \"0x1a7ee0a7efc70ed7429edef069a1dd001fbff378748d91f17ab1876dc6d10392\"\n}"
})
headers = {
   'Content-Type': 'application/json',
   'X-API-KEY': 'BQY55Sc3614Jdm3QGs7cNPihY14WkoEy'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
