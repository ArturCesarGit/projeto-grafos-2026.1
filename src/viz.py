import os
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