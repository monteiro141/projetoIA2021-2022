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
posicao_atual=[-1,-1]

G = nx.Graph()
dictLoja = {}
'''
Importar do csv para o grafo
'''
with open('grafo.csv',newline="") as csvfile:
    mapa = csv.reader(csvfile, delimiter=",", quotechar="|")
    for trajeto in mapa:
        G.add_edge(trajeto[0], trajeto[1], weight=float(trajeto[2]))
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

'''
Verifica o género das pessoas que o robô passa
'''
def viewGender(objeto):
    transform_Nomes=treinador_Nomes.transform(features([objeto]))
    transform_Array = transform_Nomes.toarray()
    previsao = arvore_Decisao.predict(transform_Array)
    if int(previsao[0]) == 0:
        mulher[0]=mulher[1]
        mulher[1]=objeto

def checkZone(zona, pos):
    for i in dictLoja:
       if int(dictLoja[i]['XDIR']) >= pos[0] >= int(dictLoja[i]['XESQ']) and int(dictLoja[i]['YCIMA']) <= pos[1] <= int(dictLoja[i]['YBAIXO']):
           dictLoja[i]['zona'] = zona

def viewZone(pos):
    for i in dictLoja:
       if int(dictLoja[i]['XDIR']) >= pos[0] >= int(dictLoja[i]['XESQ']) and int(dictLoja[i]['YCIMA']) <= pos[1] <= int(dictLoja[i]['YBAIXO']):
           return i
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
    posicao_atual[0]=posicao[0]
    posicao_atual[1]=posicao[1]
    if posicao_anterior!=posicao and objeto_anterior!=objetos:
        objeto_anterior.clear()
        for i in objetos:
            if 'adulto' in i or 'criança' in i or 'funcionário' in i:        
                viewGender(i.split('_')[1])
            if 'zona' in i:
                checkZone(i.split('_')[1], posicao)
            objeto_anterior.append(i)
        posicao_anterior[0]=posicao[0]
        posicao_anterior[1]=posicao[1]

def calcularDistancia2Pontos(ponto1, ponto2):
    pontoMedio=[]
    pontoMedio.append((int(dictLoja[ponto2]['XESQ']) + int(dictLoja[ponto2]['XDIR'])) /2)
    pontoMedio.append((int(dictLoja[ponto2]['YCIMA']) + int(dictLoja[ponto2]['YBAIXO'])) /2)
    distancia= ((pontoMedio[0]-ponto1[0])**2 + (pontoMedio[1]-ponto1[1])**2)**0.5
    return distancia
def resp1():
    #Qual foi a penúltima pessoa do sexo feminino que viste?
    if mulher[0] == 'null':
        print("O robô ainda não passou pelo menos por duas mulheres, logo não existe penúltima pessoa do sexo feminino")
    else:
        print("Penúltima pessoa do sexo feminino vista foi a", mulher[0])
    pass

def resp2():
    #Em que tipo de zona estás agora?
    print(dictLoja[viewZone(posicao_atual)]['zona'])
    

def resp3():
    #Qual o caminho para a papelaria?
    #verificar se existe papelaria
    conhece=False
    
    for i in dictLoja:    
        if dictLoja[i]['zona'] == 'papelaria':
            papelaria=i
            conhece=True
            break
    if conhece:
        caminho=nx.astar_path(G,viewZone(posicao_atual), papelaria)
        caminhoFinal=[]
        for i in caminho:
            if '_' in i:
                auxiliar=i.split('_')[0]
                if auxiliar not in caminhoFinal:
                    caminhoFinal.append(auxiliar)
            else:
                caminhoFinal.append(i)
        print(caminhoFinal)
    else:
        print("Não sabe onde é o papelaria.")
        
        
    

def resp4():
    #Qual a distância até ao talho?
    conhece=False
    for i in dictLoja:    
        if dictLoja[i]['zona'] == 'talho':
            talho=i
            conhece=True
            break
    if conhece:
        gnext=G
        zona_atual=viewZone(posicao_atual)
        ligacoes_zona=gnext.edges([zona_atual])

        for i in ligacoes_zona:
            gnext.add_edge('P_A', i[1], weight=calcularDistancia2Pontos(posicao_atual,i[1]))
        
        caminho=nx.astar_path(gnext,'P_A', talho)
        distancia=0
        for i in range(0, (len(caminho)-1)):
            distancia+=gnext.get_edge_data(caminho[i], caminho[i+1])["weight"]
        print("Distância da posição atual ao talho é",round(distancia,2))
    else:
        print("Não sabe onde é o talho.")

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
