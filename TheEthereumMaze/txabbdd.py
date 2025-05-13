import sqlite3
# Simulación de transacciones de Ethereum
DB_PATH = "eth_tx_index.db"

# Datos de las transacciones simuladas
transacciones = [
    {
        "from_address": "0xA1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1A1",
        "to_address": "0xB1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1",
        "value_eth": 0.1,
        "tx_hash": "txA",
        "block_number": 10001,
        "timestamp": "2024-05-10 12:00:00"
    },
    {
        "from_address": "0xB1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1B1",
        "to_address": "0xC1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1",
        "value_eth": 0.1,
        "tx_hash": "txB",
        "block_number": 10002,
        "timestamp": "2024-05-10 12:10:00"
    },
    {
        "from_address": "0xC1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1",
        "to_address": "0xD1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1D1",
        "value_eth": 0.1,
        "tx_hash": "txC",
        "block_number": 10003,
        "timestamp": "2024-05-10 12:20:00"
    }
]

# Conectar a la base de datos y crear un cursor
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Insertar transacciones simuladas
for tx in transacciones:
    cursor.execute("""
        INSERT INTO transactions (from_address, to_address, value_eth, tx_hash, block_number, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        tx["from_address"], 
        tx["to_address"], 
        tx["value_eth"], 
        tx["tx_hash"], 
        tx["block_number"], 
        tx["timestamp"]
    ))

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("✅ Transacciones insertadas correctamente en la base de datos.")
