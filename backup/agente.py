"""
agente.py

criar aqui as funções que respondem às perguntas
e quaisquer outras que achem necessário criar

colocar aqui os nomes e número de aluno:
43994, Bruno Monteiro
44149, Alexandre Monteiro

"""
import time
import networkx as nx

G = nx.Graph()
dictLoja = {}
"""
Importar do csv para o grafo
"""
import csv
with open('grafo.csv',newline="") as csvfile:
    mapa = csv.reader(csvfile, delimiter=",", quotechar="|")
    for trajeto in mapa:
        G.add_edge(trajeto[0], trajeto[1], weight=int(trajeto[2]))

with open("dictLoja.csv") as f:
    csv_list = [[val.strip() for val in r.split(",")] for r in f.readlines()]

(_, *header), *data = csv_list
for row in data:
    key, *values = row   
    dictLoja[key] = {key: value for key, value in zip(header, values)}

def printNodes():
    print(dictLoja)
    print(dictLoja['S7'])
        
def work(posicao, bateria, objetos):
    # esta função é invocada em cada ciclo de clock
    # e pode servir para armazenar informação recolhida pelo agente
    # recebe:
    # posicao = a posição atual do agente, uma lista [X,Y]
    # bateria = valor de energia na bateria, um número inteiro >= 0
    # objetos = o nome do(s) objeto(s) próximos do agente, uma string

    # podem achar o tempo atual usando, p.ex.
    # time.time()
    pass
	
def resp1():
    printNodes()
    #pass

def resp2():
    pass

def resp3():
    pass

def resp4():
    pass

def resp5():
    pass

def resp6():
    pass

def resp7():
    pass

def resp8():
    pass
