import heapq

def dijkstra(grafo, origem, destino):
    # Se a origem ou destino não existirem, retorna vazio
    if origem not in grafo.get_nodes() or destino not in grafo.get_nodes():
        return float('inf'), []

    # Dicionário para guardar a menor distância conhecida até cada nó (começa no infinito)
    distancias = {no: float('inf') for no in grafo.get_nodes()}
    distancias[origem] = 0
    
    # Dicionário para lembrar de onde viemos (para reconstruir o caminho no final)
    caminho_anterior = {no: None for no in grafo.get_nodes()}
    
    # Fila de prioridade: guarda tuplas (distancia_acumulada, no_atual)
    fila = [(0, origem)]
    
    while fila:
        distancia_atual, no_atual = heapq.heappop(fila)
        
        # Se chegamos no destino, podemos parar de procurar
        if no_atual == destino:
            break
            
        # Se achamos um caminho mais longo do que o que já conhecemos, ignoramos
        if distancia_atual > distancias[no_atual]:
            continue
            
        # Analisando os vizinhos do nó atual
        for vizinho, dados_aresta in grafo.get_neighbors(no_atual).items():
            peso_aresta = float(dados_aresta['peso'])
            nova_distancia = distancia_atual + peso_aresta
            
            # Se encontramos um caminho mais curto para o vizinho, atualizamos!
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                caminho_anterior[vizinho] = no_atual
                heapq.heappush(fila, (nova_distancia, vizinho))
                
    # Se o destino continua com distância infinita, é porque não tem caminho
    if distancias[destino] == float('inf'):
        return float('inf'), []
        
    # Reconstruindo o caminho do destino de volta para a origem
    caminho_final = []
    no_passo = destino
    
    while no_passo is not None:
        caminho_final.insert(0, no_passo)
        no_passo = caminho_anterior[no_passo]
        
    return round(distancias[destino], 2), caminho_final