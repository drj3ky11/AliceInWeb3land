import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import sys
# Busca destinos comunes, pinta un grafo con TODO LO QUE HAY EN EL CSV
def load_csv(file_path):
    return pd.read_csv(file_path)


def find_common_destinations(df1, df2):
    dest1 = set(df1['Destino'])
    dest2 = set(df2['Destino'])
    common = dest1.intersection(dest2)
    results = {}
    for d in common:
        origins1 = df1[df1['Destino'] == d]['Origen'].unique().tolist()
        origins2 = df2[df2['Destino'] == d]['Origen'].unique().tolist()
        results[d] = {'origenes_csv_a': origins1, 'origenes_csv_e': origins2}
    return results


def build_graph(df_list, labels=None):
    G = nx.DiGraph()
    for i, df in enumerate(df_list):
        label = labels[i] if labels and i < len(labels) else f'csv_{i}'
        for _, row in df.iterrows():
            src = row['Origen']
            dst = row['Destino']
            tx_hash = row['Hash TX']
            # Añadir nodos y arista con atributo
            G.add_node(src)
            G.add_node(dst)
            G.add_edge(src, dst, tx=tx_hash, source=label)
    return G


def draw_graph(G):
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    plt.figure(figsize=(12, 12))
    # nodos
    nx.draw_networkx_nodes(G, pos, node_size=500, alpha=0.8)
    # aristas
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=10, width=1.5)
    # etiquetas de nodos
    nx.draw_networkx_labels(G, pos, font_size=10)
    # etiquetas de aristas (Hash TX)
    edge_labels = nx.get_edge_attributes(G, 'tx')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    plt.axis('off')
    plt.title('Gráfico de Wallets y Transacciones')
    plt.tight_layout()
    plt.show()


def main(a_file='a.csv', e_file='e.csv'):
    # Carga archivos
    df_a = load_csv(a_file)
    df_e = load_csv(e_file)

    # Encuentra destinos comunes
    common = find_common_destinations(df_a, df_e)
    if common:
        print("Destinos comunes encontrados:")
        for dest, origins in common.items():
            print(f"\nDestino: {dest}")
            print(f"  Orígenes en a.csv: {origins['origenes_csv_a']}")
            print(f"  Orígenes en e.csv: {origins['origenes_csv_e']}")
    else:
        print("No se encontraron destinos comunes entre los CSV.")

    # Gráfico
    G = build_graph([df_a, df_e], labels=['a.csv', 'e.csv'])
    draw_graph(G)

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        main(sys.argv[1], sys.argv[2])
    else:
        main()