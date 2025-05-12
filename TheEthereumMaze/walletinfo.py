import requests
from decimal import Decimal

# Atacando al nodo
NODE_URL = "http://localhost:8545"
DIRECCION = "0x...."  # Dirección a consultar

# JSON-RPC
payload = {
    "jsonrpc": "2.0",
    "method": "eth_getBalance",
    "params": [DIRECCION, "latest"], 
    "id": 1
}

response = requests.post(NODE_URL, json=payload).json()

# El balance está en wei
if "result" in response:
    balance_wei = int(response["result"], 16)  
    balance_eth = balance_wei / 10**18  # 1 ETH = 10^18 wei
    print(f"Balance: {balance_eth:.6f} ETH")
else:
    print("Error:", response.get("error", "Desconocido"))
    