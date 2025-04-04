# Conexão Inteligente: Otimização da Rede de Fibra Óptica em Áreas Urbanas
# Arthur Cezar da Silveira Lima - 10409172
# Gabriel Morgado Nogueira - 10409493

import os
import re

# Criamos a classe Grafo para representar a estrutura de um grafo não orientado com pesos nas arestas.
class Grafo:
    def __init__(self):
        # Definimos o tipo como 2, indicando grafo não orientado com pesos
        self.tipo = 2
        self.vertices = {}  # Utilizamos um dicionário para mapear índices aos nomes dos vértices
        self.arestas = []   # Armazenamos as arestas como tuplas (u, v, peso)

    # Esse método nos permite ler a estrutura do grafo a partir de um arquivo
    def ler_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            self.tipo = int(f.readline().strip())  # Lemos o tipo do grafo
            n = int(f.readline().strip())  # Lemos a quantidade de vértices
            self.vertices = {}
            for _ in range(n):
                linha = f.readline().strip()
                # Utilizamos expressão regular para extrair o índice e o nome do vértice
                match = re.match(r'(\d+)\s+"(.+?)"\s+\d+', linha)
                if match:
                    idx = int(match.group(1))
                    nome = match.group(2)
                    self.vertices[idx] = nome
            m = int(f.readline().strip())  # Lemos a quantidade de arestas
            self.arestas = []
            for _ in range(m):
                u, v, peso = f.readline().strip().split()
                self.arestas.append((int(u), int(v), float(peso)))  # Armazenamos as arestas com seus pesos

    # Esse método grava o grafo atual em um arquivo, no mesmo formato que o de leitura
    def gravar_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(f"{self.tipo}\n")
            f.write(f"{len(self.vertices)}\n")
            for idx, nome in self.vertices.items():
                f.write(f'{idx} "{nome}" 0\n')  # Optamos por manter o terceiro campo como 0
            f.write(f"{len(self.arestas)}\n")
            for u, v, peso in self.arestas:
                f.write(f"{u} {v} {peso}\n")

    # Usamos esse método para adicionar um novo vértice ao grafo
    def inserir_vertice(self, nome):
        novo_idx = max(self.vertices.keys(), default=-1) + 1  # Geramos o próximo índice disponível
        self.vertices[novo_idx] = nome
        print(f"Vértice '{nome}' adicionado com índice {novo_idx}.")

    # Este método nos permite adicionar uma nova aresta entre dois vértices existentes
    def inserir_aresta(self, u, v, peso):
        if u in self.vertices and v in self.vertices:
            self.arestas.append((u, v, peso))
            print(f"Aresta {u} - {v} com peso {peso} adicionada.")
        else:
            print("Erro: vértices inválidos.")

    # Com este método, conseguimos remover um vértice e todas as arestas conectadas a ele
    def remover_vertice(self, idx):
        if idx in self.vertices:
            del self.vertices[idx]
            # Filtramos as arestas para remover as que envolvem o vértice excluído
            self.arestas = [(u, v, p) for u, v, p in self.arestas if u != idx and v != idx]
            print(f"Vértice {idx} removido com suas arestas.")
        else:
            print("Erro: vértice não encontrado.")

    # Aqui removemos uma aresta específica entre dois vértices
    def remover_aresta(self, u, v):
        antes = len(self.arestas)
        self.arestas = [t for t in self.arestas if not (t[0] == u and t[1] == v or t[0] == v and t[1] == u)]
        depois = len(self.arestas)
        print(f"Arestas removidas: {antes - depois}")

    # Esse método imprime todo o conteúdo atual do grafo, útil para conferência
    def mostrar_arquivo(self):
        print(f"Tipo do grafo: {self.tipo}")
        print("Vértices:")
        for idx, nome in self.vertices.items():
            print(f"  {idx}: {nome}")
        print("Arestas:")
        for u, v, peso in self.arestas:
            print(f"  {u} - {v} : {peso} km")

    # Aqui exibimos o grafo no formato de lista de adjacência
    def mostrar_grafo(self):
        adj = {idx: [] for idx in self.vertices}  # Inicializamos a lista de adjacência
        for u, v, peso in self.arestas:
            adj[u].append((v, peso))
            adj[v].append((u, peso))  # Como é não orientado, adicionamos nos dois sentidos
        for idx in sorted(adj):
            conexoes = ", ".join([f"{v}({peso})" for v, peso in adj[idx]])
            print(f"{idx} -> {conexoes}")

    # Com este método, geramos a forma reduzida do grafo: sua árvore geradora mínima
    def forma_reduzida(self):
        if not self.arestas:
            print("Grafo vazio ou sem arestas.")
            return

        parent = {}

        # Função auxiliar para encontrar o representante de um conjunto
        def find(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]  # Compressão de caminho
                v = parent[v]
            return v

        # Função auxiliar para unir dois conjuntos
        def union(u, v):
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[rv] = ru
                return True
            return False

        # Inicializamos cada vértice como seu próprio conjunto
        for v in self.vertices:
            parent[v] = v

        # Ordenamos as arestas pelo peso para aplicar o algoritmo de Kruskal
        arestas_ordenadas = sorted(self.arestas, key=lambda x: x[2])
        agm = []  # Aqui vamos armazenar a árvore geradora mínima

        for u, v, peso in arestas_ordenadas:
            if union(u, v):
                agm.append((u, v, peso))

        print("\nForma reduzida Gr(G) — Árvore Geradora Mínima:")
        for u, v, peso in agm:
            print(f"{u} - {v} : {peso} km")

    # Verificamos se o grafo é conexo e, se for, mostramos a forma reduzida
    def verificar_conexidade(self):
        visitado = set()

        # Função auxiliar para realizar busca em profundidade
        def dfs(v):
            visitado.add(v)
            for x in self.arestas:
                if x[0] == v or x[1] == v:
                    viz = x[1] if x[0] == v else x[0]
                    if viz not in visitado:
                        dfs(viz)

        if not self.vertices:
            print("Grafo vazio.")
            return

        inicio = next(iter(self.vertices))  # Pegamos um vértice qualquer para iniciar a DFS
        dfs(inicio)

        if len(visitado) == len(self.vertices):
            print("Grafo conexo.")
            self.forma_reduzida()
        else:
            print("Grafo desconexo.")


# Criamos esse menu para facilitar a interação com o usuário na aplicação
def menu():
    grafo = Grafo()
    while True:
        print("\n=== Conexão Inteligente: Otimização da Rede de Fibra Óptica ===")
        print("1. Ler dados do arquivo grafo.txt")
        print("2. Gravar dados no arquivo grafo.txt")
        print("3. Inserir vértice")
        print("4. Inserir aresta")
        print("5. Remover vértice")
        print("6. Remover aresta")
        print("7. Mostrar conteúdo do arquivo")
        print("8. Mostrar grafo (lista de adjacência)")
        print("9. Verificar conexidade e exibir Gr(G)")
        print("0. Encerrar aplicação")
        op = input("Opção: ")

        # Aqui tratamos cada opção do menu chamando os métodos da classe Grafo
        if op == '1':
            grafo.ler_arquivo('grafo.txt')
        elif op == '2':
            grafo.gravar_arquivo('grafo.txt')
        elif op == '3':
            nome = input("Nome do novo vértice: ")
            grafo.inserir_vertice(nome)
        elif op == '4':
            u = int(input("Índice do vértice origem: "))
            v = int(input("Índice do vértice destino: "))
            peso = float(input("Peso (distância em km): "))
            grafo.inserir_aresta(u, v, peso)
        elif op == '5':
            idx = int(input("Índice do vértice a remover: "))
            grafo.remover_vertice(idx)
        elif op == '6':
            u = int(input("Índice do vértice origem: "))
            v = int(input("Índice do vértice destino: "))
            grafo.remover_aresta(u, v)
        elif op == '7':
            grafo.mostrar_arquivo()
        elif op == '8':
            grafo.mostrar_grafo()
        elif op == '9':
            grafo.verificar_conexidade()
        elif op == '0':
            print("Encerrando aplicação...")
            break
        else:
            print("Opção inválida.")

# Chamamos a função menu quando o script é executado diretamente
if __name__ == '__main__':
    menu()