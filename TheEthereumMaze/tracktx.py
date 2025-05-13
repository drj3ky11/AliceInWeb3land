import sqlite3
from pyvis.network import Network

# Base de datos
DB_PATH = "eth_tx_index.db"

# Conectamos a la base de datos
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Función para obtener la primera transacción recibida por una dirección
def primera_tx_recibida(address):
    cursor.execute("""
        SELECT from_address, to_address, value_eth, tx_hash, block_number, timestamp
        FROM transactions
        WHERE LOWER(to_address) = LOWER(?)
        ORDER BY block_number ASC
        LIMIT 1
    """, (address,))
    return cursor.fetchone()

# Construcción recursiva del camino A ← B ← C ← D
def construir_camino(address_inicial, pasos=3):
    camino = []
    actual = address_inicial

    for _ in range(pasos):
        tx = primera_tx_recibida(actual)
        if tx:
            from_addr, to_addr, value, tx_hash, block, timestamp = tx
            camino.append({
                "from": from_addr,
                "to": to_addr,
                "value": value,
                "tx_hash": tx_hash,
                "block": block,
                "timestamp": timestamp
            })
            actual = from_addr
        else:
            break  # Si no encuentra transacción, termina

    return camino

# 🕸 Visualizar con PyVis
def visualizar_camino(camino, address_inicial):
    net = Network(directed=True, height="600px", width="100%", bgcolor="#ffffff", font_color="black")

    net.add_node(address_inicial, label="A\n"+address_inicial[:6] + "...", color="red")

    for i, tx in enumerate(camino):
        from_addr = tx["from"]
        to_addr = tx["to"]
        label = f"{tx['value']:.5f} ETH\n{tx['timestamp'][:10]}"
        net.add_node(from_addr, label=from_addr[:6] + "...", color="orange" if i == 0 else "gray")
        net.add_node(to_addr, label=to_addr[:6] + "...", color="red" if i == 0 else "gray")
        net.add_edge(from_addr, to_addr, label=label)

    #net.show("camino_tx.html")
    net.write_html("camino_tx.html")
    print("✅ Grafo generado en camino_tx.html")

# 🚀 Ejecutar
if __name__ == "__main__":
    address_inicial = input("Introduce la dirección Ethereum de inicio: ").strip()
    camino = construir_camino(address_inicial, pasos=3)

    if camino:
        visualizar_camino(camino, address_inicial)
    else:
        print("No se encontraron transacciones entrantes para esa dirección.")

    conn.close()
