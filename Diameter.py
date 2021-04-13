from typing import List
import random


class Vertice:
    """
    Representa um vértice de um grafo com um número e uma lista de adjacências.
    """

    def __init__(self, num: int) -> None:
        """
        Cria um novo vértice com o número num e com uma lista de adjacências vazia.

        Em geral este construtor não é cha
        mado diretamente mas é chamado pelo
        construtor da classe Grafo.
        """
        self.num = num
        self.adj: List[Vertice] = []

    def __str__(self) -> str:
        return "Vertice(%d)" % (self.num,)


class Grafo:
    """
    Representa um grafo não orientado
    """

    def __init__(self, n: int) -> None:
        """
        Cria um novo grafo com n vértices com os números 0, 1, ..., n-1.
        """
        self.vertices = [Vertice(i) for i in range(n)]
        self.numAresta = 0

    def addAresta(self, u: int, v: int):
        """
        Adiciona a aresta (u, v) ao grafo e aresta (v, u).

        u e v precisam ser vértices válidos, isto é precisam ser um valor
        entre 0 e n - 1, onde n é a quantidade de vértices do grafo.

        Este método não verifica se a aresta (u, v) já existe no grafo.
        """
        self.vertices[u].adj.append(self.vertices[v])
        self.vertices[v].adj.append(self.vertices[u])
        self.numAresta = self.numAresta + 1

    def Numvertices(self) -> int:
        # retorna o numero de verticee no grafo
        return len(self.vertices)

    def getVertice(self, n: int) -> Vertice:
        # retorna o vertice n
        return self.vertices[n]


class queue:
    # contrutor de uma fila, recebe como parametro o tamnho da fila a ser criada
    def __init__(self, tamanho: int) -> None:
        self.inicio = 0
        self.final = 0
        self.queue = [-1]*tamanho

    # coloca um item no inicio fila
    def enfileira(self, objeto: int):
        self.queue[self.inicio] = objeto
        if self.inicio < len(self.queue)-1:
            self.inicio = self.inicio+1

    # tira um item no final da fila e retorna ele
    def desinfileira(self) -> None:
        if self.isFilaVazia():
            return None
        else:
            objeto = self.queue[self.final]
            self.queue[self.final] = -1
            self.final = self.final+1
            return objeto

    # verifica se a fila está vazia
    def isFilaVazia(self) -> bool:
        return self.final == self.inicio

    # imprime as caracteristicas de uma fila
    def Printarfila(self):
        print(self.queue)
        print(self.final)
        print(self.inicio)


# funçao BFS recebe como parametro um grafo g, o numero do vertice inicial s>=0 e o tamanho do grafo n>0
# retorna um arrray que indica a distancias dos vertices em relação a s
def BFS(g: Grafo, s: int, n: int) -> List[int]:
    # O array visistados marca True para os vertices visistados
    visitado = [False]*n
    Q = queue(n)
    # inicializa o vetor d com o tamanho do grafo g
    # d[i] é  adistancia do vertice i em relação a s
    distancia = [-1]*n
    # ïnicializa o vertice s como ja visitado a sua distancia sendo 0 e coloca ele na fila na posiçao 0
    distancia[s] = 0
    visitado[s] = True
    Q.enfileira(s)
    while not Q.isFilaVazia():
        vPai = g.getVertice(Q.desinfileira())
        visitado[vPai.num] = True
        for vFilho in vPai.adj:
            if not visitado[vFilho.num]:
                Q.enfileira(vFilho.num)
                distancia[vFilho.num] = distancia[vPai.num]+1
                visitado[vFilho.num] = True
    # retorna o vetor d que é o vetor das distancias dos vertices em relação a s
    return distancia

# função que calcula o diametro de um arvores
# Retorna o Diametro de uma arvore


def Diameter(g: Grafo) -> int:
    # pega um vertice aleatório do grafo g
    numVertices = g.Numvertices()
    s = random.randint(0, numVertices-1)
    # a é o vertice que ob  tece valor máximo obtido no BFS
    distanciaDeS = BFS(g, s, numVertices)
    a = distanciaDeS.index(max(distanciaDeS))
    # b é o vertice que obtece valor máximo obtido no BFS
    distanciaDeA = BFS(g, a, numVertices)
    b = distanciaDeA.index(max(distanciaDeA))
    return distanciaDeA[b]

# gera uma arvore aleatória com n vertices
# retorna um grafo com n vertices


def random_tree_radom_walk(n: int) -> Grafo:
    g = Grafo(n)
    visitado = [False]*n
    u = random.randint(0, n-1)
    visitado[u] = True
    while(g.numAresta < n-1):
        v = random.randint(0, n-1)
        if not visitado[v]:
            g.addAresta(u, v)
            visitado[v] = True
        u = v
    return g

# calcula a média(500 execuçôes) do diametro de uma arvore aleatorio co numero de vertices n
# retorna a media


def teste_random_tree(n: int) -> int:
    total = 0
    for _ in range(500):
        g = random_tree_radom_walk(n)
        total += Diameter(g)
    return total/500


# testes grafo de tamanho 1,5 e 11
g = Grafo(6)
g.addAresta(0, 1)
g.addAresta(0, 3)
g.addAresta(1, 4)
g.addAresta(2, 4)
g.addAresta(2, 5)
g.addAresta(3, 1)
g.addAresta(4, 3)
assert BFS(g, 0, 6) == [0, 1, 3, 1, 2, 4]
assert Diameter(g) == 4

g = Grafo(11)
g.addAresta(0, 1)
g.addAresta(0, 3)
g.addAresta(0, 2)
g.addAresta(2, 4)
g.addAresta(2, 5)
g.addAresta(3, 6)
g.addAresta(4, 8)
g.addAresta(4, 7)
g.addAresta(5, 9)
g.addAresta(9, 10)
assert Diameter(g) == 6
assert BFS(g, 0, 11) == [0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4]


g = Grafo(1)
assert Diameter(g) == 0
assert BFS(g, 0, 1) == [0]

media250 = teste_random_tree(250)
print("Diametro de uma arvore com 250 arestas: ", media250)
media500 = teste_random_tree(500)
print("Diametro de uma arvore com 500 arestas: ", media500)
media750 = teste_random_tree(750)
print("Diametro de uma arvore com 750 arestas: ", media750)
media1000 = teste_random_tree(1000)
print("Diametro de uma arvore com 1000 arestas: ", media1000)
media1250 = teste_random_tree(1250)
print("Diametro de uma arvore com 1250 arestas: ", media1250)
media1500 = teste_random_tree(1500)
print("Diametro de uma arvore com 1500 arestas: ", media1500)
media1750 = teste_random_tree(1750)
print("Diametro de uma arvore com 1750 arestas: ", media1750)
media2000 = teste_random_tree(2000)
print("Diametro de uma arvore com 2000 arestas: ", media2000)
