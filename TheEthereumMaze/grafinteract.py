import pandas as pd
import sys
from pyvis.network import Network
# Destinos comunes con un grafo interactivo	usando PyVis
def load_csv(file_path):
    return pd.read_csv(file_path)

def find_common_destinations(df1, df2):
    return set(df1['Destino']).intersection(set(df2['Destino']))

def build_pyvis_graph(df1, df2, common_dest):
    net = Network(height="750px", width="100%", directed=True, bgcolor="#ffffff", font_color="black")
    net.force_atlas_2based()

    # Para evitar nodos duplicados
    added_nodes = set()

    for df, source in zip([df1, df2], ['a.csv', 'e.csv']):
        sub_df = df[df['Destino'].isin(common_dest)]
        for _, row in sub_df.iterrows():
            src = row['Origen']
            dst = row['Destino']
            tx = row['Hash TX']

            if src not in added_nodes:
                net.add_node(src, label=src)
                added_nodes.add(src)
            if dst not in added_nodes:
                net.add_node(dst, label=dst)
                added_nodes.add(dst)

            net.add_edge(src, dst, title=f"{source}: {tx}", label=source)

    return net

def main(a_file='a.csv', e_file='e.csv'):
    df_a = load_csv(a_file)
    df_e = load_csv(e_file)

    common_dest = find_common_destinations(df_a, df_e)
    if not common_dest:
        print("No se encontraron destinos comunes.")
        return

    print(f"Se encontraron {len(common_dest)} destinos comunes.")
    net = build_pyvis_graph(df_a, df_e, common_dest)

    output_file = "grafo_interactivo.html"
    net.show(output_file)
    print(f"Grafo guardado en: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        main(sys.argv[1], sys.argv[2])
    else:
        main()
