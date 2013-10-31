# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:31:46 2013

@author: IgKuznetsov
"""

from pandas import read_csv, DataFrame
from sklearn import cross_validation, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc
from pandas.tools.plotting import scatter_matrix
import pylab as pl
from sklearn import linear_model


data = read_csv('train.csv', header=None)

target = data[0]
train = data.drop(0, axis=1)

scatter_matrix(data, alpha=0.2)

kfold = 10
itog = DataFrame(index=xrange(kfold))

#Строим модели
model = linear_model.LinearRegression()
scores = cross_validation.cross_val_score(model, train, target, cv = kfold)
itog.insert(len(itog.columns),'LinearRegression',scores)


model = svm.SVC(kernel='linear')
scores = cross_validation.cross_val_score(model, train, target, cv = kfold)
itog.insert(len(itog.columns),'SVM Liner',scores)
model = svm.SVC(kernel='poly')
scores = cross_validation.cross_val_score(model, train, target, cv = kfold)
itog.insert(len(itog.columns),'SVM Poly',scores)
model = svm.SVC(kernel='rbf', gamma=0.7)
scores = cross_validation.cross_val_score(model, train, target, cv = kfold)
itog.insert(len(itog.columns),'SVM rbf',scores)

for n in range(5,15,4):   
    model = KNeighborsClassifier(n_neighbors = n)
    scores = cross_validation.cross_val_score(model, train, target, cv = kfold)
    FieldName = str(model)[:str(model).find('(')] + ' ' + str(model.n_neighbors)
    itog.insert(len(itog.columns), FieldName, scores)

model = BernoulliNB()
scores = cross_validation.cross_val_score(model, train, target, cv = kfold)
itog.insert(len(itog.columns),'BernulNaiveBaes',scores)

for n in range(20,81,30):
    model = RandomForestClassifier(n_estimators = n, max_features='log2')
    scores = cross_validation.cross_val_score(model, train, target, cv = kfold)
    FieldName = str(model)[:str(model).find('(')] + ' ' + str(model.n_estimators)
    itog.insert(len(itog.columns), FieldName, scores)


SumInfo = itog.describe().transpose()

SumInfo['mean'].plot(kind='bar', legend=False)
print SumInfo['mean']

#рисуем ROC
pl.clf()
ROCtrainTRN, ROCtestTRN, ROCtrainTRG, ROCtestTRG = cross_validation.train_test_split(train, target, test_size=0.25)
model = svm.SVC(kernel='linear', probability = True)
probas = model.fit(ROCtrainTRN, ROCtrainTRG).predict_proba(ROCtestTRN)
fpr, tpr, thresholds = roc_curve(ROCtestTRG, probas[:, 1])
roc_auc  = auc(fpr, tpr)
pl.plot(fpr, tpr, label='%s ROC curve (area = %0.2f)' % ('SVM_Liner',roc_auc))

model = RandomForestClassifier(n_estimators = 80, max_features='log2')
probas = model.fit(ROCtrainTRN, ROCtrainTRG).predict_proba(ROCtestTRN)
fpr, tpr, thresholds = roc_curve(ROCtestTRG, probas[:, 1])
roc_auc  = auc(fpr, tpr)
pl.plot(fpr, tpr, label='%s ROC curve (area = %0.2f)' % ('RandomForest 80',roc_auc))



pl.plot([0, 1], [0, 1], 'k--')
pl.xlim([0.0, 1.0])
pl.ylim([0.0, 1.0])
pl.xlabel('False Positive Rate')
pl.ylabel('True Positive Rate')
pl.legend(loc="lower right")
pl.show()



