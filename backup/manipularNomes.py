import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

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

sample_name = ["Carlos"]
vect = cv.transform(sample_name).toarray()
print(clf.predict(vect))