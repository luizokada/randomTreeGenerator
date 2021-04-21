from typing import List
import random
import time
import math


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
        return self.final == self.inicio+1

    # imprime as caracteristicas de uma fila
    def Printarfila(self):
        print(self.queue)
        print(self.final)
        print(self.inicio)

    def extractMin(self, chaves: List[int]) -> int:
        u = chaves.index(min(chaves))
        self.queue[self.queue.index(u)] = -1
        self.final = self.final+1
        chaves[u] = math.inf
        return u


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
# escre no display o numero de vertices do grado mais a media dos diametros
def teste_random_tree():
    total = 0
    parametroinit = 250
    arvore = False
    tempoinicio = time.perf_counter()
    while parametroinit <= 2000:
        total = 0
        media = 0
        for _ in range(500):
            arvore = False
            g = random_tree_radom_walk(parametroinit)
            arvore = isTree(g, parametroinit)
            if arvore:
                media = media+1
                total += Diameter(g)
        print(parametroinit, " ", total/media)
        parametroinit = parametroinit + 250
    tempofinal = time.perf_counter()
    print(f"{tempofinal-tempoinicio: 0.4f}")


def testeRandomTreeKruskal():
    total = 0
    parametroinit = 250
    arvore = False
    tempoinicio = time.perf_counter()
    while parametroinit <= 2000:
        total = 0
        media = 0
        for _ in range(500):
            arvore = False
            g = randomTreeKruskal(parametroinit)
            arvore = isTree(g, parametroinit)
            if arvore:
                media = media+1
                total += Diameter(g)
        print(parametroinit, " ", total/media)
        parametroinit = parametroinit + 250
    tempofinal = time.perf_counter()
    print(f"{tempofinal-tempoinicio: 0.4f}")

#verifica se o grafo é uma arvore
def isTree(g: Grafo, n: int) -> bool:
    ciclo = False
    visitado = [False]*n
<<<<<<< HEAD
    vertice = g.getVertice(random.randint(0, n-1))
    arvore = achaCiclos(g, visitado, vertice, -1)
    for i in range(n):
        if not visitado[i]:
            return False
    return not arvore


def achaCiclos(g: Grafo, visitado: List[bool], vertice: Vertice, Pai: int):
=======
    vertice = g.getVertice(random.randint(0,n-1))
    ciclo = achaCiclos(g, visitado, vertice, -1)
    #verifica se todos os vertices estão conectados a arvore
    for i in range(n):
        if not visitado[i]:
            return false
    return not ciclo

#verifica se um grafo nao orientado possui um ciclo
def achaCiclos(g: Grafo, visitado: List[bool], vertice: Vertice, Pai:int):
>>>>>>> f3bc6295aac81c0be299c95936eb73dfa96e1e6e
    visitado[vertice.num] = True
    vPai = g.getVertice(vertice.num)
    for vFilho in vPai.adj:
        if not visitado[vFilho.num]:
            if achaCiclos(g, visitado, vFilho, vertice.num):
                return True
        elif vFilho.num != Pai:
            return True
    return False


def geraGrafoCompleto(n: int) -> Grafo:
    g = Grafo(n)
    for i in range(n):
        for j in range(i+1, n):
            g.addAresta(i, j)
    return g

# def extraiMin(q: queue, Arestas: List[List[float]]) -> int:


def addPesoAresta(g: Grafo) -> List[List[float]]:
    n = g.Numvertices()
    a = [[math.inf for col in range(n)] for row in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            peso = 0
            while(peso == 0):
                peso = random.random()
            a[i][j] = peso
            a[j][i] = peso
    return a


def randomTreeKruskal(n: int) -> Grafo:
    g = geraGrafoCompleto(n)
    arestas = addPesoAresta(g)
    arvore = MSTKruskal(g, arestas)
    return arvore


def MSTPrim(g: Grafo, Arestas: List[List[float]], vertice: int) -> Grafo:
    arvore = Grafo(g.Numvertices())
    Chaves = [math.inf]*g.Numvertices()
    Pai = [-1]*g.Numvertices()
    q = queue(g.Numvertices())
    Chaves[vertice] = 0
    for i in range(g.Numvertices()):
        q.enfileira(i)
    while not q.isFilaVazia():
        q.Printarfila()
        u = q.extractMin(Chaves)
        if Pai[u] != -1:
            arvore.addAresta(Pai[u], u)
        u = g.getVertice(u)
        for vFilho in u.adj:
            if vFilho.num in q.queue and Arestas[u.num][vFilho.num] < Chaves[vFilho.num]:
                Pai[vFilho.num] = u.num
                Chaves[vFilho.num] = Arestas[u.num][vFilho.num]
    return arvore


def randomTreePrim(n: int) -> Grafo:
    g = geraGrafoCompleto(n)
    arestas = addPesoAresta(g)
    vertice = random.randint(0, g.Numvertices()-1)
    arvore = MSTPrim(g, arestas, vertice)
    return arvore


def MSTKruskal(g: Grafo, Arestas: List[List[float]]) -> Grafo:
    A = Grafo(g.Numvertices())
    Pai = [0]*g.Numvertices()
    Rank = [0]*g.Numvertices()
    for i in range(g.Numvertices()):
        MakeSet(Rank, Pai, i)
    PesoOrdenado = []
    for i in range(g.Numvertices()):
        for j in range(i+1, g.Numvertices()):
            PesoOrdenado.append(({"v1": i, "v2": j}, Arestas[i][j]))
    PesoOrdenado.sort(key=selecionaCrtierioParaOrdenar)
    for i in range(g.numAresta):
        u = PesoOrdenado[i][0]["v1"]
        v = PesoOrdenado[i][0]["v2"]
        if FindSet(Pai, u) != FindSet(Pai, v):
            A.addAresta(u, v)
            Union(u, v, Rank, Pai)
    return A


def selecionaCrtierioParaOrdenar(el) -> int:
    return el[1]


def MakeSet(rank: List[int], Pai: List[int], vertice: int):
    Pai[vertice] = vertice
    rank = 0


def FindSet(Pai: List[int], vertice: int) -> int:
    if(Pai[vertice] != vertice):
        Pai[vertice] = FindSet(Pai, Pai[vertice])
    return Pai[vertice]


def Link(u: int, v: int, rank: List[int], Pai: List[int]):
    if(rank[u] > rank[v]):
        Pai[v] = u
    else:
        Pai[u] = v
        if rank[u] == rank[v]:
            rank[v] = +1


def Union(u: int, v: int, rank: List[int], Pai: List[int]):
    Link(FindSet(Pai, u), FindSet(Pai, v), rank, Pai)


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

g = Grafo(3)
g.addAresta(0, 1)
g.addAresta(1, 2)
g.addAresta(0, 2)
assert isTree(g, 3) == False
g = Grafo(3)
g.addAresta(0, 1)
g.addAresta(1, 2)
assert isTree(g, 3) == True
<<<<<<< HEAD
# teste_random_tree()
g = Grafo(5)
# a = addPesoAresta(g)
g = randomTreeKruskal(4)
assert isTree(g, g.Numvertices()) == True
# testeRandomTreeKruskal()
g = randomTreePrim(250)
d = isTree(g, 250)
print(d)
=======

teste_random_tree()



>>>>>>> f3bc6295aac81c0be299c95936eb73dfa96e1e6e
