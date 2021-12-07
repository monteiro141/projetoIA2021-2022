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
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier


#Global variables
mulher=['null','null']
posicao_anterior=[-1,-1]
posicao_anterior_distance=[-1,-1]
objeto_anterior = []
posicao_atual=[-1,-1]
posicao_atual_distance=[-1,-1]
posicoes_questao5=[]

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
        'first3-letters': name[0:3], # First 3 letters
        'last-letter': name[-1],
        'last2-letters': name[-2:],
        'last3-letters': name[-3:],
    }

features = np.vectorize(features)
#print(features(["Paula", "Joaquim", "Miguel","Susana","Cláudia","Elsa"]))

nomes_features = features(nomes)
genero_features = genero

nomes_features_treino, nomes_features_teste, genero_features_treino, genero_features_teste = train_test_split(nomes_features, genero_features, test_size=0.05, random_state=42)

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
    if int(previsao[0]) == 0 and mulher[1]!=objeto:
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

def distanceWalked(posicaoAnterior,posicaoAtual):
    return ((posicaoAtual[0]-posicaoAnterior[0])**2+(posicaoAtual[1] - posicaoAnterior[1])**2)**0.5

distanciaTotal=0
currentTime=time.time()
startTime=0
state=0

def timeanddistanceWalked(posicaoAnterior, posicaoAtual):
    global distanciaTotal,startTime,state

    if(state==0):
        if posicaoAnterior != posicaoAtual and posicaoAnterior != [-1,-1]:
            startTime = time.time()
            state = 1
    if state==1:
        if posicaoAnterior == posicaoAtual:
            state = 2
        else:
            distanciaTotal += distanceWalked(posicaoAnterior,posicaoAtual)
    if state ==2:
        posicoes_questao5.append([distanciaTotal,round((time.time()-startTime),2)])
        state=0
        distanciaTotal=0

currentTimeBattery=time.time()
inicialBattery=100
stateBattery=0
BatteryData=[]
currentBattery=0
def predictBattery():
    global state, currentTimeBattery, inicialBattery,BatteryData, currentBattery

    if round(time.time()-currentTimeBattery,2)>=1 and currentBattery != 0 and currentBattery <= inicialBattery:
        currentTimeBattery=time.time()
        BatteryData.append([inicialBattery, inicialBattery - currentBattery])
        inicialBattery=currentBattery
    elif currentBattery > inicialBattery:
        inicialBattery=currentBattery

        


def work(posicao, bateria, objetos):
    global currentTime, posicao_anterior_distance, posicao_atual_distance, posicoes_questao5, currentBattery
    # esta função é invocada em cada ciclo de clock
    # e pode servir para armazenar informação recolhida pelo agente
    # recebe:
    # posicao = a posição atual do agente, uma lista [X,Y]
    # bateria = valor de energia na bateria, um número inteiro >= 0
    # objetos = o nome do(s) objeto(s) próximos do agente, uma string

    # podem achar o tempo atual usando, p.ex.
    # time.time()
    #pass
    if posicao_anterior_distance==[-1,-1]:
        posicao_anterior_distance[0]=posicao[0]
        posicao_anterior_distance[1]=posicao[1]
    
    posicao_atual[0]=posicao[0]
    posicao_atual[1]=posicao[1]
    posicao_atual_distance[0]=posicao[0]
    posicao_atual_distance[1]=posicao[1]
    
    currentBattery=bateria
    predictBattery()
    
    timeanddistanceWalked(posicao_anterior_distance,posicao_atual_distance)
    posicao_anterior_distance[0]=posicao_atual_distance[0]
    posicao_anterior_distance[1]=posicao_atual_distance[1]

    
    
    
    if posicao_anterior!=posicao and objeto_anterior!=objetos:
        objeto_anterior.clear()
        for i in objetos:
            if 'adulto' in i or 'criança' in i or 'funcionário' in i:        
                viewGender(i.split('_')[1])
            if 'zona' in i:
                checkZone(i.split('_')[1], posicao)
            if 'caixa' in i:
                checkZone(i.split('_')[0], posicao)
            objeto_anterior.append(i)
        posicao_anterior[0]=posicao[0]
        posicao_anterior[1]=posicao[1]

def calcularDistancia2Pontos(ponto1, ponto2):
    pontoMedio=[]
    pontoMedio.append((int(dictLoja[ponto2]['XESQ']) + int(dictLoja[ponto2]['XDIR'])) /2)
    pontoMedio.append((int(dictLoja[ponto2]['YCIMA']) + int(dictLoja[ponto2]['YBAIXO'])) /2)
    distancia= ((pontoMedio[0]-ponto1[0])**2 + (pontoMedio[1]-ponto1[1])**2)**0.5
    return distancia
    
def conhecerLocaisEDistanciaAteEles(Local):
    conhece=False
    for i in dictLoja:    
        if dictLoja[i]['zona'] == Local:
            zona=i
            conhece=True
            break
    if conhece and dictLoja[viewZone(posicao_atual)]['zona'] == Local:
        return 0
    if conhece and dictLoja[viewZone(posicao_atual)]['zona'] != Local:
        gnext=G.copy()
        zona_atual=viewZone(posicao_atual)
        ligacoes_zona=gnext.edges([zona_atual])
        for i in ligacoes_zona:
            gnext.add_edge('P_A', i[1], weight=calcularDistancia2Pontos(posicao_atual,i[1]))
        
        caminho=nx.astar_path(gnext,'P_A', zona)
        distancia=0
        for i in range(0, (len(caminho)-1)):
            distancia+=gnext.get_edge_data(caminho[i], caminho[i+1])["weight"]
        return round(distancia,2)
    else:
        return -1
    pass

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
    pass
    

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
    pass
        
        
    

def resp4():
    #Qual a distância até ao talho?
    conhecerTalho = conhecerLocaisEDistanciaAteEles("talho")
    if conhecerTalho > 0:
        print("Distância da posição atual ao talho é",conhecerTalho)
    elif conhecerTalho == 0:
        print("Chegou ao talho.")
    else:
        print("Não sabe onde é o talho.")
    pass

def resp5():
    #Quanto tempo achas que demoras a ir de onde estás até à caixa?
    '''
    X distancia a percorrer
    Y tempo que demora a percorrer
    '''

    conhecerCaixa = conhecerLocaisEDistanciaAteEles("caixa")
    if conhecerCaixa >0:
        N = len(posicoes_questao5) 

        xiyi = 0 
        xi = 0
        yi = 0
        xi2 = 0

        for x,y in posicoes_questao5:
            xiyi += x*y
            xi += x
            yi +=  y
            xi2 += x**2

        w1 = ((N*xiyi) - xi * yi) / ((N*xi2) - xi**2)
        w0 = (yi - w1*xi)/N 
        print("Demora cerca de",round(w1*conhecerCaixa+w0,2),"segundos a chegar à caixa.")
    
    elif conhecerCaixa ==0:
        print("Ja está na caixa.")

    else:
        print("Não sabe onde é a caixa.")
    pass

def resp6():
    #Quanto tempo achas que falta até ficares com metade da bateria que tens agora?
    global BatteryData
   
    

    N = len(BatteryData) 

    xiyi = 0 
    xi = 0
    yi = 0
    xi2 = 0

    for x,y in BatteryData:
        xiyi += x*y
        xi += x
        yi +=  y
        xi2 += x**2

    w1 = ((N*xiyi) - xi * yi) / ((N*xi2) - xi**2)
    w0 = (yi - w1*xi)/N
   
    halfBattery=currentBattery/2
    #batteryLoss=w1*currentBattery+w0
    #print("PERDA:",batteryLoss)
    secondsToDrain=0
    
    while halfBattery > 0:
        batteryLoss=w1*halfBattery+w0
        secondsToDrain+=1
        halfBattery=halfBattery -batteryLoss
        print("BATERIA:",halfBattery)
    print("Para ficar com metade da bateria que tem agora demora",secondsToDrain)
    """
    Implementar SVM para ver se há melhorias
    """
    pass

def resp7():
    #Qual é a probabilidade da próxima pessoa a encontrares ser uma criança?

    pass

def resp8():
    #Qual é a probabilidade de encontrar um adulto numa zona se estiver lá uma criança mas não estiver lá um carrinho?
    pass
