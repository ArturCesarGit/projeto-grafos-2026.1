import os
import json
import csv
from src.graphs.io import load_graph

def exportar_metricas():
    # Garante que a pasta out/ existe
    os.makedirs('out', exist_ok=True)
    
    grafo = load_graph()
    todos_nos = grafo.get_nodes()
    
    # ---------------------------------------------------------
    # 1. MÉTRICAS GLOBAIS -> out/global.json
    # ---------------------------------------------------------
    metricas_globais = {
        "ordem": grafo.get_order(),
        "tamanho": grafo.get_size(),
        "densidade": round(grafo.get_density(), 4)
    }
    
    with open('out/global.json', 'w', encoding='utf-8') as f:
        json.dump(metricas_globais, f, indent=4)
        
    print("✅ out/global.json gerado.")

    # ---------------------------------------------------------
    # 2. GRAUS DOS AEROPORTOS -> out/graus.csv
    # ---------------------------------------------------------
    lista_graus = []
    for no in todos_nos:
        lista_graus.append([no, grafo.get_degree(no)])
    
    # Ordenando do maior para o menor grau (opcional, mas fica mais bonito)
    lista_graus.sort(key=lambda x: x[1], reverse=True)
    
    with open('out/graus.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['aeroporto', 'grau'])
        writer.writerows(lista_graus)
        
    print("✅ out/graus.csv gerado.")

    # ---------------------------------------------------------
    # 3. MÉTRICAS POR REGIÃO -> out/regioes.json
    # ---------------------------------------------------------
    # Primeiro, vamos agrupar os aeroportos por região
    regioes = {}
    for no in todos_nos:
        regiao = grafo.nodes[no]['regiao']
        if regiao not in regioes:
            regioes[regiao] = []
        regioes[regiao].append(no)
        
    metricas_regioes = {}
    
    for nome_regiao, aeroportos_regiao in regioes.items():
        v = len(aeroportos_regiao)
        # Contando as arestas que existem apenas DENTRO dessa região
        e = 0
        for i in range(len(aeroportos_regiao)):
            for j in range(i + 1, len(aeroportos_regiao)):
                aero1 = aeroportos_regiao[i]
                aero2 = aeroportos_regiao[j]
                if aero2 in grafo.adj.get(aero1, {}):
                    e += 1
                    
        # Calculando a densidade regional
        densidade = 0.0
        if v >= 2:
            densidade = (2 * e) / (v * (v - 1))
            
        metricas_regioes[nome_regiao] = {
            "ordem": v,
            "tamanho": e,
            "densidade": round(densidade, 4)
        }
        
    with open('out/regioes.json', 'w', encoding='utf-8') as f:
        json.dump(metricas_regioes, f, indent=4, ensure_ascii=False)
        
    print("✅ out/regioes.json gerado.")

    # ---------------------------------------------------------
    # 4. EGO-NETWORKS -> out/ego_aeroportos.csv
    # ---------------------------------------------------------
    ego_dados = []
    
    for no in todos_nos:
        grau = grafo.get_degree(no)
        vizinhos = list(grafo.adj.get(no, {}).keys())
        
        # A ego-network inclui o nó central + seus vizinhos
        nos_ego = [no] + vizinhos
        v_ego = len(nos_ego)
        
        # Contando as arestas dentro da ego-network
        e_ego = 0
        for i in range(len(nos_ego)):
            for j in range(i + 1, len(nos_ego)):
                a1 = nos_ego[i]
                a2 = nos_ego[j]
                if a2 in grafo.adj.get(a1, {}):
                    e_ego += 1
                    
        densidade_ego = 0.0
        if v_ego >= 2:
            densidade_ego = (2 * e_ego) / (v_ego * (v_ego - 1))
            
        ego_dados.append([no, grau, v_ego, e_ego, round(densidade_ego, 4)])
        
    with open('out/ego_aeroportos.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['aeroporto', 'grau', 'ordem_ego', 'tamanho_ego', 'densidade_ego'])
        writer.writerows(ego_dados)
        
    print("✅ out/ego_aeroportos.csv gerado.")
    print("\n🎉 Todas as métricas da Parte 1 foram exportadas com sucesso para a pasta 'out/'!")

if __name__ == '__main__':
    exportar_metricas()