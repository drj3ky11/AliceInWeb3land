from web3 import Web3
import sqlite3
from datetime import datetime

# Creamos un pequelo index de los últimos 100 bloques de la red Ethereum para pruebas
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

if not w3.isConnected():
    print("No se pudo conectar a la red Ethereum.")
    exit()

conn = sqlite3.connect("eth_tx_index.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    tx_hash TEXT PRIMARY KEY,
    from_address TEXT,
    to_address TEXT,
    value_eth REAL,
    block_number INTEGER,
    timestamp TEXT
)
""")

conn.commit()


latest_block = w3.eth.block_number
start_block = latest_block - 99

print(f"Indexando bloques desde {start_block} hasta {latest_block}")


for block_number in range(start_block, latest_block + 1):
    block = w3.eth.get_block(block_number, full_transactions=True)
    block_timestamp = datetime.utcfromtimestamp(block.timestamp).isoformat()

    for tx in block.transactions:
        if tx.to:  # Solo transacciones no contratos creados
            value_eth = tx.value / 1e18  # Evitar overflown en python

            cursor.execute("""
            INSERT OR IGNORE INTO transactions (tx_hash, from_address, to_address, value_eth, block_number, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                tx.hash.hex(),
                tx["from"],
                tx["to"],
                value_eth,
                block_number,
                block_timestamp
            ))

    print(f"Bloque {block_number} procesado ({len(block.transactions)} txs)")

conn.commit()
conn.close()

print("✅ Indexación completada.")
