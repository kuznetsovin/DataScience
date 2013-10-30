# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:31:46 2013

@author: IgKuznetsov
"""

from pandas import read_csv, DataFrame
#from sklearn.preprocessing import LabelEncoder
from sklearn import cross_validation, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import roc_curve, auc
import pylab as pl

data = read_csv('train.csv', header=None)

target = data[0]
train = data.drop(0, axis=1)

kfold = 10

model = svm.SVC()
itog = DataFrame(index=xrange(kfold))
scores = cross_validation.cross_val_score(model, train, target, cv = kfold)
itog.insert(len(itog.columns),'SVM_Liner',scores)

model = svm.SVC(kernel='poly', degree=3)
scores = cross_validation.cross_val_score(model, train, target, cv = kfold)
itog.insert(len(itog.columns),'SVM_Poly',scores)

model = svm.SVC(kernel='rbf', gamma=0.7)
scores = cross_validation.cross_val_score(model, train, target, cv = kfold)
itog.insert(len(itog.columns),'SVM_rbf',scores)

model = KNeighborsClassifier(n_neighbors =3)
scores = cross_validation.cross_val_score(model, train, target, cv = kfold)
itog.insert(len(itog.columns),'Neighbors 3',scores)

model = KNeighborsClassifier(n_neighbors =5)
scores = cross_validation.cross_val_score(model, train, target, cv = kfold)
itog.insert(len(itog.columns),'Neighbors 5',scores)

model = KNeighborsClassifier(n_neighbors =10)
scores = cross_validation.cross_val_score(model, train, target, cv = kfold)
itog.insert(len(itog.columns),'Neighbors 10',scores)

model = BernoulliNB()
scores = cross_validation.cross_val_score(model, train, target, cv = kfold)
itog.insert(len(itog.columns),'BernulNaiveBaes',scores)

SumInfo = itog.describe()


print itog
print SumInfo

SumInfo[SumInfo.index == 'mean'].plot(kind='bar', legend=False)
#
#ROCtrainTRN, ROCtestTRN, ROCtrainTRG, ROCtestTRG = cross_validation.train_test_split(train, target, test_size=0.25)
#model = svm.SVC()
#model.probability = True
#probas = model.fit(ROCtrainTRN, ROCtrainTRG).predict_proba(ROCtestTRN)
#
#fpr, tpr, thresholds = roc_curve(ROCtestTRG, probas[:, 1])
#roc_auc  = auc(fpr, tpr)
#
#pl.clf()
#pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
#pl.plot([0, 1], [0, 1], 'k--')
#pl.xlim([0.0, 1.0])
#pl.ylim([0.0, 1.0])
#pl.xlabel('False Positive Rate')
#pl.ylabel('True Positive Rate')
#pl.title('Receiver operating characteristic example')
#pl.legend(loc="lower right")
#pl.show()