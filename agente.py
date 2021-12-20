"""
agente.py

criar aqui as funções que respondem às perguntas
e quaisquer outras que achem necessário criar

43994, Bruno Miguel Gonçalves Monteiro
44149, Alexandre Salcedas Monteiro

"""

#Import das funções utilizadas
import time
import csv
import numpy as np
import networkx as nx
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
import pyAgrum as gum


#Variaveis globais
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
Importar o grafo do csv para um grafo G
'''
with open('grafo.csv',newline="") as csvfile:
    mapa = csv.reader(csvfile, delimiter=",", quotechar="|")
    for trajeto in mapa:
        G.add_edge(trajeto[0], trajeto[1], weight=float(trajeto[2]))

'''
Importa o dicionario com zonas e corredores para um dicionário chamado dictLoja
'''
with open("dictLoja.csv") as f:
    csv_list = [[val.strip() for val in r.split(",")] for r in f.readlines()]
(_, *header), *data = csv_list
for row in data:
    key, *values = row   
    dictLoja[key] = {key: value for key, value in zip(header, values)}

#Coloca os valores de adultos, cariinhos,crianças e funcionários a 0 no inicio da execução do programa
for i in dictLoja:
    dictLoja[i]['adultos'] = 0
    dictLoja[i]['carrinhos'] = 0
    dictLoja[i]['criancas'] = 0
    dictLoja[i]['funcionarios'] = 0

'''
Lê do raparigas_rapazes.csv a lista de nomes do sexo feminino e masculino. Guarda-se os nomes num array e o correspondente genero num array
'''
data = np.loadtxt('raparigas_rapazes.csv',delimiter=",",dtype=str,encoding="UTF-8")
nomes = data[:,0]
genero = data[:,1]


'''
Função responsável pela elaboração das características de um dado nome
'''
def features(name):
    name = name.lower()
    return {
        'first-letter': name[0],     # primeira 1 letra
        'first2-letters': name[0:2], # primeiras 2 letras
        'first3-letters': name[0:3], # primeiras 3 letras
        'last-letter': name[-1],     # ultima letra
        'last2-letters': name[-2:],  # ultimas 2 letras
        'last3-letters': name[-3:],  # ultimas 3 letras
    }

''''
Linha 84 a 101 para a pergunta 1
'''
features = np.vectorize(features)

#converte os nomes em features
nomes_features = features(nomes)
genero_features = genero

#Criação dos conjuntos de treino para criarmos a árvore de decisão
nomes_features_treino, nomes_features_teste, genero_features_treino, genero_features_teste = train_test_split(nomes_features, genero_features, test_size=0.05, random_state=42)

treinador_Nomes = DictVectorizer()

treinador_Nomes.fit_transform(nomes_features_treino)

#Torna as features dos nomes em vetores de números para poder ser usado na árvore de decisão
my_xfeatures =treinador_Nomes.transform(nomes_features_treino)
#criação da árvore de decisão
arvore_Decisao = DecisionTreeClassifier()
arvore_Decisao.fit(my_xfeatures, genero_features_treino)


'''
Verifica o género da pessoa que o robô observa.
Irá dar predict se o nome da dada pessoa é do género feminino.
Caso seja e seja diferente da que observou anteriormente irá guardá-lo no array
Caso seja do sexo masculino, não irá alterar o array
'''
def viewGender(objeto):
    transform_Nomes=treinador_Nomes.transform(features([objeto]))
    transform_Array = transform_Nomes.toarray()
    previsao = arvore_Decisao.predict(transform_Array)
    if int(previsao[0]) == 0 and mulher[1]!=objeto:
        mulher[0]=mulher[1]
        mulher[1]=objeto


'''
Coloca o nome da zona, caso o robô encontrar, numa dada zona, o nome da mesma.
Ou seja, tendo em conta a posição do robô e a zona que identificou irá ser alterado no dicionário a designação da zona
'''
def checkZone(zona, pos):
    for i in dictLoja:
       if int(dictLoja[i]['XDIR']) >= pos[0] >= int(dictLoja[i]['XESQ']) and int(dictLoja[i]['YCIMA']) <= pos[1] <= int(dictLoja[i]['YBAIXO']):
           dictLoja[i]['zona'] = zona

'''
Tendo em conta a posição do agente irá devolver a posição no dicionário dictLoja, em que a posição do robô corresponde a essa dada zona 
'''
def viewZone(pos):
    for i in dictLoja:
       if int(dictLoja[i]['XDIR']) >= pos[0] >= int(dictLoja[i]['XESQ']) and int(dictLoja[i]['YCIMA']) <= pos[1] <= int(dictLoja[i]['YBAIXO']):
           return i

'''
Função utilizada para calcular a distância entre duas posições
'''
def distanceWalked(posicaoAnterior,posicaoAtual):
    return ((posicaoAtual[0]-posicaoAnterior[0])**2+(posicaoAtual[1] - posicaoAnterior[1])**2)**0.5

#Variáveis utilizadas para ajudar a processar dados essenciais para a pergunta 5
distanciaTotal=0
currentTime=time.time()
startTime=0
state=0

'''
Função utilizada para recolher dados essenciais para a pergunta 5.
Autómato:
Estado 0 - regista o inicio do andar do robô e transita para o estado 1.
Estado 1 - Se o robô parar irá transitar para o estado 2.
           Caso não pare iremos ir somando a distância percorrida pelo robô entre as posição anterior e a atual
Estado 2 - É dado append num array os pares [distancia total, tempo percorrido].
           Transita para o estado 0 e a distância é colocada a 0.
'''
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


#Variáveis utilizadas para ajudar a processar dados essenciais para a pergunta 6
currentTimeBattery=time.time()
inicialBattery=100
stateBattery=0
BatteryData=[]
currentBattery=0

'''
Função que a cada segundo irá dar append num array os pares [bateria inicial, quantidade perdida]
'''
def predictBattery():
    global state, currentTimeBattery, inicialBattery,BatteryData, currentBattery


    if round(time.time()-currentTimeBattery,2)>=1 and currentBattery != 0 and currentBattery <= inicialBattery:
        currentTimeBattery=time.time()
        BatteryData.append([inicialBattery, inicialBattery - currentBattery])
        inicialBattery=currentBattery
    elif currentBattery > inicialBattery:
        inicialBattery=currentBattery

#Variável utilizada para registar os adultos, carrinhos, crianças e empregados que o robõ encontra ao longo do seu movimento pelo supermercado    
Actual_Adults_Karts_Employees=[]

def work(posicao, bateria, objetos):
    global currentTime, posicao_anterior_distance, posicao_atual_distance, posicoes_questao5, currentBattery, Actual_Adults_Karts_Employees
    # esta função é invocada em cada ciclo de clock
    # e pode servir para armazenar informação recolhida pelo agente
    # recebe:
    # posicao = a posição atual do agente, uma lista [X,Y]
    # bateria = valor de energia na bateria, um número inteiro >= 0
    # objetos = o nome do(s) objeto(s) próximos do agente, uma string

    # podem achar o tempo atual usando, p.ex.
    # time.time()
    #pass
    
    #Na primeira execução da função work irá guardar a posição anterior como a posição atual.
    if posicao_anterior_distance==[-1,-1]:
        posicao_anterior_distance[0]=posicao[0]
        posicao_anterior_distance[1]=posicao[1]
    
    #obtem a posição atual a cada ciclo de clock
    posicao_atual[0]=posicao[0]
    posicao_atual[1]=posicao[1]
    posicao_atual_distance[0]=posicao[0]
    posicao_atual_distance[1]=posicao[1]
    
    #As linhas 224 e 225 são responsáveis pela recolha de dados para a realização da pergunta 6
    currentBattery=bateria
    predictBattery()
    
    #função utilizada para recolher dados que serão necessários para a pergunta 5
    timeanddistanceWalked(posicao_anterior_distance,posicao_atual_distance)
    #Guarda a posição anterior que será essencial para a execução seguinte da função acima
    posicao_anterior_distance[0]=posicao_atual_distance[0]
    posicao_anterior_distance[1]=posicao_atual_distance[1]

    
    
    #
    if posicao_anterior!=posicao and objeto_anterior!=objetos:
        objeto_anterior.clear()
        for i in objetos:
            #Caso encontre adultos, crianças e funcionários irá ver o seu respetivo género 
            if 'adulto' in i or 'criança' in i or 'funcionário' in i:        
                viewGender(i.split('_')[1])
            #Caso identifique uma zona, irá ver se já a conhece, caso não conheça irá guardar a identificação da zona
            if 'zona' in i:
                checkZone(i.split('_')[1], posicao)
            #Caso identifique a caixa, irá ver se já a conhece, caso não conheça irá guardar a identificação da caixa
            if 'caixa' in i:
                checkZone(i.split('_')[0], posicao)
            #Irá adicionar os adultos,crianças, funcionários e carrinhos que ainda não passaram pelo robô.
            #E irá incrementar o número de cada um na sua respetiva zona
            if ('adulto' in i or 'funcionário' in i or 'carrinho' in i or 'criança' in i) and i not in Actual_Adults_Karts_Employees:
                Actual_Adults_Karts_Employees.append(i)
                currentZone = viewZone(posicao)
                if 'adulto' in i:
                    dictLoja[currentZone]['adultos'] += 1
                if 'funcionário' in i:
                    dictLoja[currentZone]['funcionarios'] += 1
                if 'carrinho' in i:
                    dictLoja[currentZone]['carrinhos'] += 1
                if 'criança' in i:
                    dictLoja[currentZone]['criancas'] += 1


            objeto_anterior.append(i)
        posicao_anterior[0]=posicao[0]
        posicao_anterior[1]=posicao[1]

'''
Função usada para calcular a distância entre um dado ponto e uma dada zona
'''
def calcularDistancia2Pontos(ponto1, ponto2):
    pontoMedio=[]
    pontoMedio.append((int(dictLoja[ponto2]['XESQ']) + int(dictLoja[ponto2]['XDIR'])) /2)
    pontoMedio.append((int(dictLoja[ponto2]['YCIMA']) + int(dictLoja[ponto2]['YBAIXO'])) /2)
    distancia= ((pontoMedio[0]-ponto1[0])**2 + (pontoMedio[1]-ponto1[1])**2)**0.5
    return distancia
    
'''
Função usada para determinar a distãncia entre o local em que o robô se encontra e o local desejado. Ex: PontoA -> Talho
'''
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
    


def resp1():
    #Qual foi a penúltima pessoa do sexo feminino que viste?
    if mulher[0] == 'null':
        print("Ainda não passei por pelo menos duas mulheres, logo não existe penúltima pessoa do sexo feminino")
    else:
        print("A penúltima pessoa do sexo feminino vista foi a", mulher[0]+".")
    pass

def resp2():
    #Em que tipo de zona estás agora?
    if dictLoja[viewZone(posicao_atual)]['zona'] == "Nao sabe":
        print("Não sei o tipo, mas estou na secção " + viewZone(posicao_atual)+".")
    else:
        print("Estou na zona " + dictLoja[viewZone(posicao_atual)]['zona']+".")
    pass
    

def resp3():
    #Qual o caminho para a papelaria?
    conhece=False
    #Verificamos se a papelaria existe
    for i in dictLoja:    
        if dictLoja[i]['zona'] == 'papelaria':
            papelaria=i
            conhece=True
            break
    #Caso exista, determina-se o caminho até à papelaria
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
        #Formata-se o caminho para dar um aspeto mais apelativo
        for i in range(0,len(caminhoFinal)-1):
            if 'S' in caminhoFinal[i] and dictLoja[caminhoFinal[i]]['zona'] != 'Nao sabe':
                print(dictLoja[caminhoFinal[i]]['zona'],"-> ",end="")
            elif 'C' in caminhoFinal[i]:
                print("Corredor",caminhoFinal[i][1],"-> ",end="")
            else:
                print(caminhoFinal[i],"-> ",end="")
        print(dictLoja[caminhoFinal[len(caminhoFinal)-1]]['zona'])
    else:
        print("Não sei onde é o papelaria.")
    pass
        
        
    

def resp4():
    # Qual a distância até ao talho?
    # Iremos chamar a função que calcula a distância desde a posição atual até ao talho. 
    conhecerTalho = conhecerLocaisEDistanciaAteEles("talho")
    if conhecerTalho > 0:
        print("Distância da posição atual ao talho é",conhecerTalho)
    elif conhecerTalho == 0:
        print("Estou no talho.")
    else:
        print("Não sei onde é o talho.")
    pass

def resp5():
    #Quanto tempo achas que demoras a ir de onde estás até à caixa?
    '''
        X: distancia a percorrer
        Y: tempo que demora a percorrer
    '''

    #Determina a distância até à caixa
    conhecerCaixa = conhecerLocaisEDistanciaAteEles("caixa")
    if conhecerCaixa >0:
        #Criação da reta de regressão
        
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
        print("Demoro cerca de",round(w1*conhecerCaixa+w0,2),"segundos a chegar à caixa.")
    
    elif conhecerCaixa ==0:
        print("Já estou na caixa.")

    else:
        print("Não sei onde é a caixa.")
    pass

def resp6():
    #Quanto tempo achas que falta até ficares com metade da bateria que tens agora?
    global BatteryData
    
    #Criação da reta de regressão
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
    battery=currentBattery
    secondsToDrain=0
    # Até ficar com metade da bateria, os segundos serão incrementados e a bateria irá perdendo de acordo com a perda de bateria prevista pela reta.
    while battery > halfBattery:
        batteryLoss=w1*battery+w0
        secondsToDrain+=1
        battery=battery-batteryLoss
    print("Para ficar com metade da bateria que tem agora demoro",secondsToDrain,"segundos")
    pass

def resp7():
    #Qual é a probabilidade da próxima pessoa a encontrares ser uma criança?
    global Actual_Adults_Karts_Employees

    #Soma-se o número de adultos, funcionários, crianças e carrinhos encontrados até ao momento pelo robô
    if len(Actual_Adults_Karts_Employees)!=0:
        TotalN=len(Actual_Adults_Karts_Employees)
        Total_Adults_Karts_Employes=[0,0,0,0]
        for i in Actual_Adults_Karts_Employees:
            if 'funcionário' in i:
                Total_Adults_Karts_Employes[2]+=1
            elif 'carrinho' in i:
                Total_Adults_Karts_Employes[1]+=1
            elif 'adulto' in i:
                Total_Adults_Karts_Employes[0]+=1
            else:
                Total_Adults_Karts_Employes[3]+=1

        
        #calcula-se a probabilidade dos adultos, funcionários, crianças e carrinhos 
        Probability_Adults_Karts_Employess=[Total_Adults_Karts_Employes[0]/TotalN,Total_Adults_Karts_Employes[1]/TotalN,Total_Adults_Karts_Employes[2]/TotalN,Total_Adults_Karts_Employes[3]/TotalN]
        
        #Criação da rede Bayesiana
        
        bayesianNetwork=gum.BayesNet('Supermercado')
        Adults=bayesianNetwork.add(gum.LabelizedVariable('Adults','Adults',2))
        Karts=bayesianNetwork.add(gum.LabelizedVariable('Karts','Karts',2))
        Child=bayesianNetwork.add(gum.LabelizedVariable('Child','Child',2))

        bayesianNetwork.addArc(Adults,Child)
        bayesianNetwork.addArc(Karts,Child)

        bayesianNetwork.cpt(Adults)[{}]=[1-Probability_Adults_Karts_Employess[0],Probability_Adults_Karts_Employess[0]]
        bayesianNetwork.cpt(Karts)[{}]=[1-Probability_Adults_Karts_Employess[1],Probability_Adults_Karts_Employess[1]]

        bayesianNetwork.cpt(Child)[{'Adults': 1,'Karts': 1}]=[0.2 , 0.8]
        bayesianNetwork.cpt(Child)[{'Adults': 1,'Karts': 0}]=[0.5, 0.5]
        bayesianNetwork.cpt(Child)[{'Adults': 0,'Karts': 1}]=[0.9, 0.1]
        bayesianNetwork.cpt(Child)[{'Adults': 0,'Karts': 0}]=[0.95 , 0.05]

        ie=gum.LazyPropagation(bayesianNetwork)

        ie.setEvidence({})
        ie.makeInference()
        print ("A probabilidade é " + str(round(ie.posterior('Child')[1],3)) + ".")
    else:
        print("Não tenho dados suficientes para dar resposta.")
    pass

def resp8():
    #Qual é a probabilidade de encontrar um adulto numa zona se estiver lá uma criança mas não estiver lá um carrinho?
    global Actual_Adults_Karts_Employees

    #Soma-se o número de adultos, funcionários, crianças e carrinhos encontrados até ao momento pelo robô
    if len(Actual_Adults_Karts_Employees)!=0:
        TotalN=len(Actual_Adults_Karts_Employees)
        Total_Adults_Karts_Employes=[0,0,0,0]
        for i in Actual_Adults_Karts_Employees:
            if 'funcionário' in i:
                Total_Adults_Karts_Employes[2]+=1
            elif 'carrinho' in i:
                Total_Adults_Karts_Employes[1]+=1
            elif 'adulto' in i:
                Total_Adults_Karts_Employes[0]+=1
            else:
                Total_Adults_Karts_Employes[3]+=1

        
        #calcula-se a probabilidade dos adultos, funcionários, crianças e carrinhos 
        Probability_Adults_Karts_Employess=[Total_Adults_Karts_Employes[0]/TotalN,Total_Adults_Karts_Employes[1]/TotalN,Total_Adults_Karts_Employes[2]/TotalN,Total_Adults_Karts_Employes[3]/TotalN]
        
        #Criação da rede Bayesiana
        
        bayesianNetwork=gum.BayesNet('Supermercado')
        Adults=bayesianNetwork.add(gum.LabelizedVariable('Adults','Adults',2))
        Karts=bayesianNetwork.add(gum.LabelizedVariable('Karts','Karts',2))
        Child=bayesianNetwork.add(gum.LabelizedVariable('Child','Child',2))

        bayesianNetwork.addArc(Adults,Child)
        bayesianNetwork.addArc(Karts,Child)

        bayesianNetwork.cpt(Adults)[{}]=[1-Probability_Adults_Karts_Employess[0],Probability_Adults_Karts_Employess[0]]
        bayesianNetwork.cpt(Karts)[{}]=[1-Probability_Adults_Karts_Employess[1],Probability_Adults_Karts_Employess[1]]

        bayesianNetwork.cpt(Child)[{'Adults': 1,'Karts': 1}]=[0.2 , 0.8]
        bayesianNetwork.cpt(Child)[{'Adults': 1,'Karts': 0}]=[0.5, 0.5]
        bayesianNetwork.cpt(Child)[{'Adults': 0,'Karts': 1}]=[0.9, 0.1]
        bayesianNetwork.cpt(Child)[{'Adults': 0,'Karts': 0}]=[0.95 , 0.05]

        # Calculo da P(A| C /\ -K) pela rede bayesiana
        ie=gum.LazyPropagation(bayesianNetwork)

        ie.setEvidence({'Child':1,'Karts':0})
        ie.makeInference()
        pobabilidade = ie.posterior('Adults')[1]
        print("A probabilidade é " +str(round(pobabilidade,3)) + ".")
    else:
        print("Não tenho dados suficientes para dar resposta.")
    
    pass
