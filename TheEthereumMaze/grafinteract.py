import csv
from pyvis.network import Network
from collections import defaultdict

def leer_csv(archivo):
    datos = []
    destinos = set()
    with open(archivo, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Saltar encabezado
        for row in reader:
            origen = row[0].strip()
            tx_hash = row[1].strip()
            destino = row[2].strip()
            datos.append((origen, tx_hash, destino))
            destinos.add(destino)
    return datos, destinos

# Leer datos de ambos archivos
a_data, a_destinos = leer_csv('a.csv')
e_data, e_destinos = leer_csv('e.csv')

# Encontrar destinos comunes
common_dest = a_destinos & e_destinos

if not common_dest:
    print("No se encontraron destinos comunes.")
    exit()

# Procesar fuentes de origen y nodos destino
origen_sources = defaultdict(set)
destino_nodes = set(common_dest)

# Actualizar fuentes para a.csv
for origen, _, destino in a_data:
    if destino in common_dest:
        origen_sources[origen].add('a')
        destino_nodes.add(destino)

# Actualizar fuentes para e.csv
for origen, _, destino in e_data:
    if destino in common_dest:
        origen_sources[origen].add('e')
        destino_nodes.add(destino)

# Crear red
net = Network(notebook=True, height="750px", width="100%", cdn_resources='remote')
net.force_atlas_2based()

# Añadir nodos origen
for origen, sources in origen_sources.items():
    if len(sources) == 2:
        color = '#FF00FF'  # Morado para ambos
    elif 'a' in sources:
        color = '#0000FF'  # Azul para a.csv
    else:
        color = '#00FF00'  # Verde para e.csv
    net.add_node(origen, label=origen, color=color)

# Añadir nodos destino
for destino in destino_nodes:
    net.add_node(destino, label=destino, color='#FF0000')  # Rojo

# Añadir aristas desde a.csv
for origen, tx_hash, destino in a_data:
    if destino in common_dest:
        net.add_edge(origen, destino, title=tx_hash, color='#0000FF')

# Añadir aristas desde e.csv
for origen, tx_hash, destino in e_data:
    if destino in common_dest:
        net.add_edge(origen, destino, title=tx_hash, color='#00FF00')

# Generar y mostrar gráfico
net.show('transacciones.html')
print("Visualización generada en 'transacciones.html'")