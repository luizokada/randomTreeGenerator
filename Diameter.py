from typing import List, Tuple
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
    # retorna a lista de adjacencia de um vertice

    def getAdjacentes(self, vertice: int) -> List[int]:
        A = []
        for i in self.getVertice(vertice).adj:
            A.append(i.num)
        return A


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

    # tira da fila o vertice que tem a menor chave
    def extractMin(self, chaves: List[int]) -> int:
        u = chaves.index(min(chaves))
        self.queue[self.queue.index(u)] = -1
        self.final = self.final+1
        chaves[u] = math.inf
        return u


"""
funçao BFS recebe como parametro um grafo g, o numero do vertice inicial s>=0 e o tamanho do grafo n>0
retorna um arrray que indica a distancias dos vertices em relação a s
"""


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


"""
 função que calcula o diametro de uma arvore
 Retorna o Diametro de uma arvore
"""


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


"""
 gera uma arvore aleatória com n vertices
 retorna um grafo com n vertices
"""


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


"""
calcula a média(500 execuçôes) do diametro de uma arvore aleatoria gerada pelo randomtreewalk
escreve no display o numero de vertices do grafo e a media dos diametros
após isso escre o tempo de execução em segundos
"""


def diameterrandomTree():
    diameters = open("results/randomTree.txt", "w")
    timearq = open("results/randomTreeTime.txt", "w")
    total = 0
    parametroinit = 250
    arvore = False
    tempoinicioexecucao = time.time()
    while parametroinit <= 2000:
        total = 0
        media = 0
        tempomedio = 0
        for _ in range(500):
            arvore = False
            tempoinit = time.time()
            g = random_tree_radom_walk(parametroinit)
            arvore = isTree(g, parametroinit)
            tempofim = time.time()
            tempomedio = tempomedio+(tempofim-tempoinit)
            if arvore:
                media = media+1
                total += Diameter(g)
            else:
                return "ERRO"
        diameters.write(str(parametroinit) + " "+str(total/media)+"\n")
        timearq.write(str(parametroinit) + " "+str(tempomedio/media)+"\n")
        parametroinit = parametroinit + 250
    tempofinalexecucao = time.time()
    timearq.write("Total: "+str(tempofinalexecucao-tempoinicioexecucao))
    timearq.close()
    diameters.close()
# calcula a média(500 execuçôes) do diametro de uma arvore aleatoria gerado com o randomtreeKruskal
# escreve no display o numero de vertices do grado mais a media dos diametros
# após isso escreve o tempo de execução em segundos


def diameterRandomTreeKruskal():
    diameters = open("results/randomTreeKruskal.txt", "w")
    timearq = open("results/randomTreeKruskalTime.txt", "w")
    total = 0
    parametroinit = 250
    arvore = False
    tempoinicioexecucao = time.time()
    while parametroinit <= 2000:
        total = 0
        media = 0
        tempomedio = 0
        for _ in range(500):
            arvore = False
            tempoinit = time.time()
            g = randomTreeKruskal(parametroinit)
            arvore = isTree(g, parametroinit)
            tempofim = time.time()
            tempomedio = tempomedio+(tempofim-tempoinit)
            if arvore:
                media = media+1
                total += Diameter(g)
            else:
                return "ERRO"
        diameters.write(str(parametroinit) + " "+str(total/media)+"\n")
        timearq.write(str(parametroinit) + " "+str(tempomedio/media)+"\n")
        parametroinit = parametroinit + 250
    tempofinalexecucao = time.time()
    timearq.write("Total: "+str(tempofinalexecucao-tempoinicioexecucao))
    timearq.close()
    diameters.close()
# calcula a média(500 execuçôes) do diametro de uma arvore aleatoria gerado com o randomtreePrim
# escreve no display o numero de vertices do grado mais a media dos diametros
# após isso escreve o tempo de execução em segundos


def diameterRandomTreePrim():
    diameters = open("results/randomTreePrim.txt", "w")
    timearq = open("results/randomTreePrimTime.txt", "w")
    total = 0
    parametroinit = 250
    arvore = False
    tempoinicioexecucao = time.time()
    while parametroinit <= 2000:
        total = 0
        media = 0
        tempomedio = 0
        for _ in range(500):
            arvore = False
            tempoinit = time.time()
            g = randomTreePrim(parametroinit)
            arvore = isTree(g, parametroinit)
            tempofim = time.time()
            tempomedio = tempomedio+(tempofim-tempoinit)
            if arvore:
                media = media+1
                total += Diameter(g)
            else:
                return "ERRO"
        diameters.write(str(parametroinit) + " "+str(total/media)+"\n")
        timearq.write(str(parametroinit) + " "+str(tempomedio/media)+"\n")
        parametroinit = parametroinit + 250
    tempofinalexecucao = time.time()
    timearq.write("Total: "+str(tempofinalexecucao-tempoinicioexecucao))
    timearq.close()
    diameters.close()
# verifica se o grafo é uma arvore


def isTree(g: Grafo, n: int) -> bool:
    ciclo = False
    visitado = [False]*n
    vertice = g.getVertice(random.randint(0, n-1))
    ciclo = achaCiclos(g, visitado, vertice, -1)
    for i in range(n):
        if not visitado[i]:
            return False
    return not ciclo

# verifica se em um grafo existe um ciclo


def achaCiclos(g: Grafo, visitado: List[bool], vertice: Vertice, Pai: int):
    visitado[vertice.num] = True
    vPai = g.getVertice(vertice.num)
    for vFilho in vPai.adj:
        if not visitado[vFilho.num]:
            if achaCiclos(g, visitado, vFilho, vertice.num):
                return True
        elif vFilho.num != Pai:
            return True
    return False

# cria um grafo completo com n vertices


def geraGrafoCompleto(n: int) -> Grafo:
    g = Grafo(n)
    for i in range(n):
        for j in range(i+1, n):
            g.addAresta(i, j)
    return g


"""
adiciona pesoas aleatorios a todas arestas de um grafo completo
os valores do peso está entre 0 e 1
"""


def addPesoAresta(g: Grafo) -> List[List[float]]:
    n = g.Numvertices()
    # cria a matriz que terá os pesos das arestas
    a = [[math.inf for col in range(n)] for row in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            peso = 0
            while(peso == 0):
                peso = random.random()
            a[i][j] = peso
            a[j][i] = peso
    return a

# retorna um arvore minima


def randomTreeKruskal(n: int) -> Grafo:
    g = geraGrafoCompleto(n)
    arestas = addPesoAresta(g)
    arvore = MSTKruskal(g, arestas)
    return arvore

# retorna um arvore minima dentro de um grafo completo


def MSTKruskal(g: Grafo, Arestas: List[List[float]]) -> Grafo:
    A = Grafo(g.Numvertices())
    Pai = [0]*g.Numvertices()
    Rank = [0]*g.Numvertices()
    for i in range(g.Numvertices()):
        MakeSet(Rank, Pai, i)
    PesoOrdenado = []
    # coloca os pesos das arestas em um dicionário
    for i in range(g.Numvertices()):
        for j in range(i+1, g.Numvertices()):
            PesoOrdenado.append((i, j, Arestas[i][j]))
    # ordena os presos dentro do dicionário
    PesoOrdenado.sort(key=selecionaCrtierioParaOrdenar)
    for (u, v, _) in PesoOrdenado:
        if FindSet(Pai, u) != FindSet(Pai, v):
            A.addAresta(u, v)
            if A.numAresta == A.Numvertices()-1:
                break
            Union(u, v, Rank, Pai)
    return A

# seleciona um campo do dicionário que serivirá como critério de ordenação


def selecionaCrtierioParaOrdenar(el: Tuple[int, int, float]) -> int:
    return el[2]


"""
define o pai de um vertice e o rank dele
por padrao o vertice é pai dele mesmo e possui rank zero no inicio
"""


def MakeSet(rank: List[int], Pai: List[int], vertice: int):
    Pai[vertice] = vertice
    rank = 0

# acha o ancestral de um vertice


def FindSet(Pai: List[int], vertice: int) -> int:
    if(Pai[vertice] != vertice):
        Pai[vertice] = FindSet(Pai, Pai[vertice])
    return Pai[vertice]

# linka dois vertices diferentes a partir do seu rank


def Link(u: int, v: int, rank: List[int], Pai: List[int]):
    if(rank[u] > rank[v]):
        Pai[v] = u
    else:
        Pai[u] = v
        if rank[u] == rank[v]:
            rank[v] = +1

# faz o link entre dois vertices denpendendo do seu rank


def Union(u: int, v: int, rank: List[int], Pai: List[int]):
    Link(FindSet(Pai, u), FindSet(Pai, v), rank, Pai)

# retorna um arvore minima


def randomTreePrim(n: int) -> Grafo:
    g = geraGrafoCompleto(n)
    arestas = addPesoAresta(g)
    vertice = random.randint(0, g.Numvertices()-1)
    arvore = MSTPrim(g, arestas, vertice)
    return arvore

# retorna um arvore minima dentro de um grafo completo


def MSTPrim(g: Grafo, Arestas: List[List[float]], vertice: int) -> Grafo:
    arvore = Grafo(g.Numvertices())
    Chaves = [math.inf]*g.Numvertices()
    Pai = [-1]*g.Numvertices()
    q = queue(g.Numvertices())
    Chaves[vertice] = 0
    # coloca todos o vertice na fila q
    for i in range(g.Numvertices()):
        q.enfileira(i)
    while not q.isFilaVazia():
        u = q.extractMin(Chaves)
        # adicona um aresta a arvore minima
        if Pai[u] != -1:
            arvore.addAresta(Pai[u], u)
        u = g.getVertice(u)
        for vFilho in u.adj:
            if q.queue[vFilho.num] != -1 and Arestas[u.num][vFilho.num] < Chaves[vFilho.num]:
                Pai[vFilho.num] = u.num
                Chaves[vFilho.num] = Arestas[u.num][vFilho.num]
    return arvore


# testes grafo de tamanho 1,5 e 11
def DiameterTest():
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

# testes da funcao isTree


def IsTreeTest():
    g = Grafo(3)
    g.addAresta(0, 1)
    g.addAresta(1, 2)
    g.addAresta(0, 2)
    assert isTree(g, 3) == False
    g = Grafo(3)
    g.addAresta(0, 1)
    g.addAresta(1, 2)
    assert isTree(g, 3) == True
    g = Grafo(5)


# teste se randomtreekruskal está gerando uma arvore
def simpleTestRandomTreeTadomWalk():
    g = random_tree_radom_walk(250)
    assert isTree(g, 250) == True

# teste das funcoes auxiliares do kruskal


def auxiliarFuncionKruskalTest():
    pai = [-1]*4
    rank = [0]*4
    a = 0
    b = 1
    c = 2
    d = 3
    MakeSet(rank, pai, a)
    MakeSet(rank, pai, b)
    MakeSet(rank, pai, c)
    MakeSet(rank, pai, d)
    assert FindSet(pai, a) == a
    assert FindSet(pai, b) == b
    assert FindSet(pai, c) == c
    assert FindSet(pai, d) == d
    Union(b, d, rank, pai)
    Union(d, a, rank, pai)
    assert rank[a] == 0
    assert rank[b] == 0
    assert rank[c] == 0
    assert rank[d] == 1
    assert FindSet(pai, a) == FindSet(pai, b)
    assert FindSet(pai, b) == FindSet(pai, a)
    assert FindSet(pai, c) != FindSet(pai, a)

# teste se randomtreekruskal está gerando uma arvore


def simpleTestKruskalandPrim():
    # randomtreeKruskal test
    g = randomTreeKruskal(250)
    assert isTree(g, g.Numvertices()) == True

    # randomtreeprim test
    g = randomTreePrim(250)
    assert isTree(g, 250) == True

    # krukal and prim example
    g = Grafo(9)
    g.addAresta(0, 1)
    g.addAresta(0, 7)
    g.addAresta(1, 2)
    g.addAresta(1, 7)
    g.addAresta(2, 3)
    g.addAresta(2, 8)
    g.addAresta(2, 5)
    g.addAresta(3, 4)
    g.addAresta(3, 5)
    g.addAresta(4, 5)
    g.addAresta(5, 6)
    g.addAresta(6, 7)
    g.addAresta(6, 8)
    g.addAresta(7, 8)

    # matriz dos pesos
    peso = [[math.inf, 4, math.inf, math.inf, math.inf, math.inf, math.inf, 8, math.inf],
            [4, math.inf, 8, math.inf, math.inf, math.inf, math.inf, 11, math.inf],
            [math.inf, 8, math.inf, 7, math.inf, 4, math.inf, math.inf, 2],
            [math.inf, math.inf, 7, math.inf, 9, 14, math.inf, math.inf, math.inf],
            [math.inf, math.inf, math.inf, 9, math.inf,
                10, math.inf, math.inf, math.inf],
            [math.inf, math.inf, 4, 14, 10, math.inf, 2, math.inf, math.inf],
            [math.inf, math.inf, math.inf, math.inf, math.inf, 2, math.inf, 1, 6],
            [math.inf, 11, math.inf, math.inf, math.inf, math.inf, 1, math.inf, 7],
            [math.inf, math.inf, 2, math.inf, math.inf, math.inf, 6, 7, math.inf]
            ]
    gr = MSTKruskal(g, peso)
    assert gr.getAdjacentes(0) == [1, 7]
    assert gr.getAdjacentes(1) == [0]
    assert gr.getAdjacentes(2) == [8, 5, 3]
    assert gr.getAdjacentes(3) == [2, 4]
    assert gr.getAdjacentes(4) == [3]
    assert gr.getAdjacentes(5) == [6, 2]
    assert gr.getAdjacentes(6) == [7, 5]
    assert gr.getAdjacentes(7) == [6, 0]
    assert gr.getAdjacentes(8) == [2]
    gr = MSTPrim(g, peso, 0)
    assert gr.getAdjacentes(0) == [1]
    assert gr.getAdjacentes(1) == [0, 2]
    assert gr.getAdjacentes(2) == [1, 8, 5, 3]
    assert gr.getAdjacentes(3) == [2, 4]
    assert gr.getAdjacentes(4) == [3]
    assert gr.getAdjacentes(5) == [2, 6]
    assert gr.getAdjacentes(6) == [5, 7]
    assert gr.getAdjacentes(7) == [6]
    assert gr.getAdjacentes(8) == [2]


def auxiliarFunctionsPrimTest():
    q = queue(5)
    chaves = [2, 3, 6, 8, 0]
    q.enfileira(0)
    q.enfileira(1)
    q.enfileira(2)
    q.enfileira(3)
    q.enfileira(4)
    assert q.extractMin(chaves) == 4
    assert q.extractMin(chaves) == 0
    assert q.extractMin(chaves) == 1
    assert q.extractMin(chaves) == 2
    assert q.extractMin(chaves) == 3
    assert q.isFilaVazia() == True


def allTests():
    DiameterTest()
    IsTreeTest()
    simpleTestRandomTreeTadomWalk()
    auxiliarFuncionKruskalTest()
    auxiliarFunctionsPrimTest()
    simpleTestKruskalandPrim()


def Diameters():
    diameterrandomTree()
    diameterRandomTreeKruskal()
    diameterRandomTreePrim()


def main():
    allTests()
    Diameters()


if __name__ == "__main__":
    main()
