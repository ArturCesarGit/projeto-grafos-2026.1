import os
import json
import matplotlib.pyplot as plt
import pandas as pd
from pyvis.network import Network

def gerar_arvore_percurso(caminho1, caminho2):
    os.makedirs('out', exist_ok=True)
    
    net = Network(height='750px', width='100%', directed=True, bgcolor='#222222', font_color='white')
    
    def adicionar_caminho(caminho, cor_no, cor_aresta):
        for i in range(len(caminho)):
            net.add_node(caminho[i], label=caminho[i], color=cor_no, size=25)
            if i > 0:
                net.add_edge(caminho[i-1], caminho[i], color=cor_aresta, width=4)

    if caminho1:
        adicionar_caminho(caminho1, cor_no='#1f874c', cor_aresta='#27ae60')
    if caminho2:
        adicionar_caminho(caminho2, cor_no='#2980b9', cor_aresta='#3498db')
        
    net.toggle_physics(False)
    net.save_graph('out/arvore_percurso.html')
    print("🎨 Arquivo out/arvore_percurso.html gerado com sucesso!")

def gerar_graficos_analiticos():
    """
    Lê os arquivos de dados e gera 4 gráficos estatísticos DIVERSOS em PNG.
    """
    import os
    import json
    import matplotlib.pyplot as plt
    import pandas as pd
    
    os.makedirs('out', exist_ok=True)
    print("\n📊 Gerando novos gráficos analíticos...")
    
    # --- GRÁFICO 1: Barras Horizontais (Top 10 Graus) ---
    df_graus = pd.read_csv('out/graus.csv')
    top10_graus = df_graus.head(10).sort_values(by='grau', ascending=True) # Ordem inversa para o gráfico horizontal ficar bonito
    
    plt.figure(figsize=(10, 6))
    plt.barh(top10_graus['aeroporto'], top10_graus['grau'], color='#3498db', edgecolor='black')
    plt.title('Top 10 Aeroportos Mais Conectados na Rede')
    plt.xlabel('Grau (Número de Conexões)')
    plt.ylabel('Aeroportos')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.savefig('out/plot_01_barras_graus.png', bbox_inches='tight')
    plt.close()
    
    # --- GRÁFICO 2: Gráfico de Pizza/Donut (Nós por Região) ---
    with open('out/regioes.json', 'r', encoding='utf-8') as f:
        regioes = json.load(f)
        
    nomes_regioes = list(regioes.keys())
    ordem_regioes = [regioes[r]['ordem'] for r in nomes_regioes]
    cores = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0']
    
    plt.figure(figsize=(8, 8))
    plt.pie(ordem_regioes, labels=nomes_regioes, autopct='%1.1f%%', startangle=140, colors=cores, wedgeprops={'edgecolor': 'black'})
    plt.title('Proporção de Aeroportos por Região do Brasil')
    plt.savefig('out/plot_02_pizza_regioes.png', bbox_inches='tight')
    plt.close()

    # --- GRÁFICO 3: Scatter Plot (Dispersão: Grau vs Densidade Ego) ---
    df_ego = pd.read_csv('out/ego_aeroportos.csv')
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df_ego['grau'], df_ego['densidade_ego'], color='#e74c3c', s=100, alpha=0.7, edgecolors='black')
    plt.title('Análise de Rede: Conectividade (Grau) vs. Densidade Local')
    plt.xlabel('Grau do Aeroporto (Quantidade de Voos)')
    plt.ylabel('Densidade da Ego-Network')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig('out/plot_03_dispersao_rede.png', bbox_inches='tight')
    plt.close()

    # --- GRÁFICO 4: Histograma de Pesos (Distâncias dos Voos) ---
    df_adj = pd.read_csv('data/adjacencias_aeroportos.csv')
    
    plt.figure(figsize=(10, 6))
    plt.hist(df_adj['peso'], bins=8, color='#2ecc71', edgecolor='black', alpha=0.8)
    plt.title('Distribuição das Distâncias dos Voos na Malha (Pesos das Arestas)')
    plt.xlabel('Distância em KM (Peso)')
    plt.ylabel('Frequência (Quantidade de Rotas)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('out/plot_04_histograma_distancias.png', bbox_inches='tight')
    plt.close()
    
    print("✅ 4 novos gráficos estatísticos gerados com sucesso na pasta 'out/'!")