"""
agente.py

criar aqui as funções que respondem às perguntas
e quaisquer outras que achem necessário criar

colocar aqui os nomes e número de aluno:
43994, Bruno Miguel Gonçalves Monteiro
44149, Alexandre Salcedas Monteiro

"""

#Import
import time
import csv
import numpy as np
import networkx as nx
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier


#Global variables
mulher=['null','null']
posicao_anterior=[-1,-1]
objeto_anterior = []

G = nx.Graph()
dictLoja = {}
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

'''
Lê nomes de rapazes e raparigas para treinar
'''
data = np.loadtxt('raparigas_rapazes.csv',delimiter=",",dtype=str,encoding="UTF-8")
nomes = data[:,0]
genero = data[:,1]


#features para os nomes
def features(name):
    name = name.lower()
    return {
        'first-letter': name[0], # First letter
        'first2-letters': name[0:2], # First 2 letters
        #'first3-letters': name[0:3], # First 3 letters
        'last-letter': name[-1],
        'last2-letters': name[-2:],
        #'last3-letters': name[-3:],
    }
'''
features = np.vectorize(features)
nomes_feature = features(nomes)
genero_feature = genero

nomes_features_treino, nomes_features_teste, genero_treino, genero_teste = train_test_split(nomes_feature, genero_feature, test_size=0.33, random_state=42)

treinadorNomes=DictVectorizer().fit_transform(nomes_features_treino)

arvore_decisao=DecisionTreeClassifier()
my_features=treinadorNomes.transform(nomes_features_treino)
arvore_decisao.fit(my_features,genero_treino)

'''

features = np.vectorize(features)
#print(features(["Paula", "Joaquim", "Miguel","Susana","Cláudia","Elsa"]))

nomes_features = features(nomes)
genero_features = genero

nomes_features_treino, nomes_features_teste, genero_features_treino, genero_features_teste = train_test_split(nomes_features, genero_features, test_size=0.33, random_state=42)

treinador_Nomes = DictVectorizer()
treinador_Nomes.fit_transform(nomes_features_treino)


 
arvore_Decisao = DecisionTreeClassifier()
my_xfeatures =treinador_Nomes.transform(nomes_features_treino)
arvore_Decisao.fit(my_xfeatures, genero_features_treino)

def viewGender(objeto):
    transform_Nomes=treinador_Nomes.transform(features([objeto]))
    transform_Array = transform_Nomes.toarray()
    previsao = arvore_Decisao.predict(transform_Array)
    print("-----", objeto)
    if int(previsao[0]) == 0:
        mulher[0]=mulher[1]
        mulher[1]=objeto
    else:
        print("HOMEM" ,objeto)

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
    pass

def resp2():
    viewGender("Ana")
    print(mulher)

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
