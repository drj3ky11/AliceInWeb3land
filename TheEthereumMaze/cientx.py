from web3 import Web3
import csv
from decimal import Decimal

# Configuración
NODE_URL = "http://localhost:8545"
ADDRESS = "0xbCA34ed5875079cC561840f3409a790769821DBc"  # Tu dirección
USDT_CONTRACT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
USDC_CONTRACT = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
CSV_FILE = "transactions.csv"
BLOCKS_TO_SCAN = 5000 # Número de bloques a escanear

w3 = Web3(Web3.HTTPProvider(NODE_URL))

def get_erc20_transfers():
    """Obtiene transferencias ERC-20 (USDT/USDC)"""
    topics = [w3.keccak(text="Transfer(address,address,uint256)").hex()]
    address = Web3.to_checksum_address(ADDRESS)
    
    logs = w3.eth.get_logs({
        "fromBlock": w3.eth.block_number - BLOCKS_TO_SCAN,
        "toBlock": "latest",
        "topics": topics,
        "address": [USDT_CONTRACT, USDC_CONTRACT]
    })
    
    transfers = []
    for log in logs:
        # Decodificar datos del log
        contract = log["address"]
        from_addr = "0x" + log["topics"][1][-20:].hex()
        to_addr = "0x" + log["topics"][2][-20:].hex()
        
        if from_addr.lower() != address.lower() and to_addr.lower() != address.lower():
            continue
        
        # Obtener símbolo y decimales
        symbol = "USDT" if contract == USDT_CONTRACT else "USDC"
        decimals = 6  # USDT/USDC usan 6 decimales
        
        # Convertir cantidad
        amount = int(log["data"].hex(), 16) / 10**decimals
        
        transfers.append({
            "tx_hash": log["transactionHash"].hex(),
            "from": from_addr,
            "to": to_addr,
            "amount": amount,
            "token": symbol
        })
    
    return transfers

def get_eth_transactions():
    """Obtiene transacciones nativas de ETH"""
    address = Web3.to_checksum_address(ADDRESS)
    transactions = []
    
    # Escanear bloques recientes
    for block_num in range(w3.eth.block_number - BLOCKS_TO_SCAN, w3.eth.block_number):
        block = w3.eth.get_block(block_num, full_transactions=True)
        
        for tx in block["transactions"]:
            if tx["to"] is None:
                continue  # Saltar despliegues de contratos
            
            is_sender = tx["from"].lower() == address.lower()
            is_receiver = tx["to"].lower() == address.lower()
            
            if is_sender or is_receiver:
                amount = w3.from_wei(tx["value"], "ether")
                
                transactions.append({
                    "tx_hash": tx["hash"].hex(),
                    "from": tx["from"],
                    "to": tx["to"],
                    "amount": float(amount),
                    "token": "ETH"
                })
    
    return transactions

def export_to_csv(transactions):
    """Exporta a CSV"""
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Origen", "Hash TX", "Destino", "Cantidad", "Token"])
        
        for tx in transactions:
            writer.writerow([
                tx["from"],
                tx["tx_hash"],
                tx["to"],
                tx["amount"],
                tx["token"]
            ])

if __name__ == "__main__":
    if not w3.is_connected():
        print("Error de conexión al nodo")
        exit()
    
    # Combinar y ordenar transacciones
    erc20_txs = get_erc20_transfers()
    eth_txs = get_eth_transactions()
    all_txs = sorted(
        erc20_txs + eth_txs,
        key=lambda x: w3.eth.get_transaction(x["tx_hash"])["blockNumber"],
        reverse=True
    )[:100]  # Últimas 100
    
    export_to_csv(all_txs)
    print(f"Exportadas {len(all_txs)} transacciones a {CSV_FILE}")