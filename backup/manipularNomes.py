import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier

'''
# Replacing All F and M with 0 and 1 respectively
df_names.sex.replace({'F':0,'M':1},inplace=True)
'''

data = np.loadtxt('raparigas_rapazes.csv',delimiter=",",dtype=str,encoding="UTF-8")

nomes = data[:,0]
genero = data[:,1]

cv = CountVectorizer()
nomesEncoded = cv.fit_transform(nomes)

X_train, X_test, y_train, y_test = train_test_split(nomesEncoded, genero, test_size=0.33, random_state=42)
clf = MultinomialNB()
clf.fit(X_train,y_train)
print(clf.score(X_test,y_test))

print("Accuracy of Model",clf.score(X_test,y_test)*100,"%")
# Accuracy of our Model
print("Accuracy of Model",clf.score(X_train,y_train)*100,"%")

sample_name = ["Elsa"]
vect = cv.transform(sample_name).toarray()
print(clf.predict(vect))
'''
0.5536423841059602
Accuracy of Model 55.36423841059602 %
Accuracy of Model 99.05352480417756 %
---------------------------------------------------------------------
'''
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

df_X = features(nomes)
df_y = genero

dfX_train, dfX_test, dfy_train, dfy_test = train_test_split(df_X, df_y, test_size=0.33, random_state=42)

dv = DictVectorizer()
dv.fit_transform(dfX_train)


 
dclf = DecisionTreeClassifier()
my_xfeatures =dv.transform(dfX_train)
dclf.fit(my_xfeatures, dfy_train)

# Build Features and Transform them
sample_name_eg = ["Asdrubalda"]
transform_dv =dv.transform(features(sample_name_eg))
vect3 = transform_dv.toarray()
# Predicting Gender of Name
# Male is 1,female = 0

arroz = dclf.predict(vect3)
print("Feature: ",arroz[0])
if int(arroz[0]) == 0:
    print("Female")
else:
    print("Male")