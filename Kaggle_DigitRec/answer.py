# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 14:29:15 2013

@author: IgKuznetsov
"""

from pandas import read_csv
from sklearn import cross_validation
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression

csv = read_csv('train.csv', header=None, skiprows=1)
joblib.dump(csv, 'digit.pkl')
dataset = joblib.load('digit.pkl')


dataset = joblib.load('digit.pkl') #сюда были свалены данные, полученные после препроцессинга

target = [x[0] for x in dataset]
train = [x[1:] for x in dataset]

glm = LogisticRegression(penalty='l1', tol=1)
scores = cross_validation.cross_val_score(glm, train, target, cv = 10)
