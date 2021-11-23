'''
agente.py

criar aqui as funções que respondem às perguntas
e quaisquer outras que achem necessário criar

colocar aqui os nomes e número de aluno:
43994, Bruno Monteiro
44149, Alexandre Monteiro

'''
import time
import networkx as nx
from sklearn import tree,preprocessing
import numpy as np
import csv
'''
Variaveis globais
'''
data = np.loadtxt('raparigas_rapazes.csv',delimiter=",",dtype=str,encoding="UTF-8")

nomes = data[:,0]
genero = data[:,1]

#nomes_float = [float(item) for item in nomes ]

le  = preprocessing.LabelEncoder()
nomes = le.fit_transform(nomes)
#le  = le.fit(nomes, genero)
nomes = nomes.reshape(1,-1).T
clf = tree.DecisionTreeClassifier().fit(nomes,genero)

print(clf.predict(le.fit_transform(['Amália'])))

G = nx.Graph()
dictLoja = {}

mulher=['null','null']
posicao_anterior=[-1,-1]
objeto_anterior = []

'''
Importar do csv para o grafo
'''

with open('grafo.csv',newline="") as csvfile:
    mapa = csv.reader(csvfile, delimiter=",", quotechar="|")
    for trajeto in mapa:
        G.add_edge(trajeto[0], trajeto[1], weight=int(trajeto[2]))
'''
Dicionario com zonas e corredores
'''
with open("dictLoja.csv") as f:
    csv_list = [[val.strip() for val in r.split(",")] for r in f.readlines()]
(_, *header), *data = csv_list
for row in data:
    key, *values = row   
    dictLoja[key] = {key: value for key, value in zip(header, values)}



def printNodes():
    print(dictLoja)
    print(dictLoja['S7'])
        
def viewGender(objetos):
    print(objetos)

def work(posicao, bateria, objetos):
    # esta função é invocada em cada ciclo de clock
    # e pode servir para armazenar informação recolhida pelo agente
    # recebe:
    # posicao = a posição atual do agente, uma lista [X,Y]
    # bateria = valor de energia na bateria, um número inteiro >= 0
    # objetos = o nome do(s) objeto(s) próximos do agente, uma string
    # podem achar o tempo atual usando, p.ex.
    # time.time()
    #pass
    if posicao_anterior!=posicao and objeto_anterior!=objetos:
        objeto_anterior.clear()
        for i in objetos:
            if 'adulto' in i or 'criança' in i or 'funcionário' in i:        
                viewGender(i.split('_')[1])
            objeto_anterior.append(i)
        posicao_anterior[0]=posicao[0]
        posicao_anterior[1]=posicao[1]
	
def resp1():
    #Qual foi a penúltima pessoa do sexo feminino que viste?
    printNodes()
    #pass

def resp2():
    #Em que tipo de zona estás agora?
    pass

def resp3():
    #Qual o caminho para a papelaria?
    pass

def resp4():
    #Qual a distância até ao talho?
    pass

def resp5():
    #Quanto tempo achas que demoras a ir de onde estás até à caixa?
    pass

def resp6():
    #Quanto tempo achas que falta até ficares com metade da bateria que tens agora?
    pass

def resp7():
    #Qual é a probabilidade da próxima pessoa a encontrares ser uma criança?
    pass

def resp8():
    #Qual é a probabilidade de encontrar um adulto numa zona se estiver lá uma criança mas não estiver lá um carrinho?

    pass

