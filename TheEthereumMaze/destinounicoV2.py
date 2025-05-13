import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import sys
# Busca destinos comunes entre dos archivos CSV y construye un grafo
def load_csv(file_path):
    return pd.read_csv(file_path)


def find_common_destinations(df1, df2):
    dest1 = set(df1['Destino'])
    dest2 = set(df2['Destino'])
    return dest1.intersection(dest2)


def build_common_subgraph(df1, df2, common_dest):
    G = nx.DiGraph()
    # Procesar df1
    for _, row in df1[df1['Destino'].isin(common_dest)].iterrows():
        src = row['Origen']
        dst = row['Destino']
        G.add_node(src)
        G.add_node(dst)
        G.add_edge(src, dst, tx=row['Hash TX'], source='a.csv')
    # Procesar df2
    for _, row in df2[df2['Destino'].isin(common_dest)].iterrows():
        src = row['Origen']
        dst = row['Destino']
        G.add_node(src)
        G.add_node(dst)
        G.add_edge(src, dst, tx=row['Hash TX'], source='e.csv')
    return G


def draw_graph(G):
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    plt.figure(figsize=(10, 10))
    # nodos
    nx.draw_networkx_nodes(G, pos, node_size=500, alpha=0.8)
    # aristas
    # Diferenciar color por origen
    edges_a = [(u, v) for u, v, d in G.edges(data=True) if d['source']=='a.csv']
    edges_e = [(u, v) for u, v, d in G.edges(data=True) if d['source']=='e.csv']
    nx.draw_networkx_edges(G, pos, edgelist=edges_a, arrowstyle='->', arrowsize=10, width=1.5)
    nx.draw_networkx_edges(G, pos, edgelist=edges_e, arrowstyle='->', arrowsize=10, width=1.5, style='dashed')
    # etiquetas de nodos
    nx.draw_networkx_labels(G, pos, font_size=10)
    # etiquetas de aristas (opcional: tx hash)
    edge_labels = { (u,v): d['tx'] for u,v,d in G.edges(data=True) }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    plt.axis('off')
    plt.title('Transacciones hacia destinos comunes')
    plt.tight_layout()
    plt.show()


def main(a_file='a.csv', e_file='e.csv'):
    # Carga archivos
    df_a = load_csv(a_file)
    df_e = load_csv(e_file)

    # Encontrar destinos comunes
    common_dest = find_common_destinations(df_a, df_e)
    if not common_dest:
        print("No se encontraron destinos comunes.")
        return
    print(f"Destinos comunes: {common_dest}")

    # Construir subgrafo y dibujar
    G_sub = build_common_subgraph(df_a, df_e, common_dest)
    draw_graph(G_sub)

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        main(sys.argv[1], sys.argv[2])
    else:
        main()