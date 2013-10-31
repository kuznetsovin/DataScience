# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 14:29:15 2013

@author: IgKuznetsov
"""

from pandas import read_csv
from sklearn import cross_validation
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn import svm

csv = read_csv('Data/train.csv')
joblib.dump(csv, 'digit.pkl')


dataset = joblib.load('digit.pkl') #сюда были свалены данные, полученные после препроцессинга


target = dataset['label']
train = dataset.drop('label',axis=1)

glm = LogisticRegression(penalty='l1', tol=1)
clf = svm.SVC()

scores = cross_validation.cross_val_score(glm, train, target, cv = 10)
scores1 = cross_validation.cross_val_score(clf, train, target, cv = 10)

print scores
print scores1
