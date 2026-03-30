import csv
from src.graphs.graph import Graph

def load_graph(caminho_aeroportos='data/aeroportos_data.csv', caminho_adjacencias='data/adjacencias_aeroportos.csv'):
    g = Graph()
    
    # 1. Lendo os nós (aeroportos)
    with open(caminho_aeroportos, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            g.add_node(row['iata'], row['cidade'], row['regiao'])
            
    # 2. Lendo as arestas (conexões)
    with open(caminho_adjacencias, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            origem = row['origem']
            destino = row['destino']
            peso = float(row['peso'])
            tipo = row['tipo_conexao']
            
            g.add_edge(origem, destino, peso, tipo)
            
    return g