# -*- coding: utf-8 -*-
from pandas import read_csv, DataFrame, Series
data = read_csv('Kaggle_Titanic/Data/train.csv')
data.pivot_table('PassengerId', 'Pclass', 'Survived', 'count').plot(kind='bar', stacked=True)
fig, axes = plt.subplots(ncols=2)
data.pivot_table('PassengerId', ['SibSp'], 'Survived', 'count').plot(ax=axes[0], title='SibSp')
data.pivot_table('PassengerId', ['Parch'], 'Survived', 'count').plot(ax=axes[1], title='Parch')
data.pivot_table('PassengerId',data.Cabin.str[0],'Survived','count').plot(kind='bar', stacked=True)

data.Cabin = data.Cabin.str[0]
data.Ticket = data.Ticket.str.replace('\.|/|','') #убираем лишние символы из серии
data.insert(len(data.columns),'SrTicket','') #добавляем столбец в котором будет записана серия
data.SrTicket = data.Ticket.str.replace(' \d*','') #в поле SrTicket записываем серию
data.Ticket = data.Ticket.str.replace('\D*','') #в поле Ticket записываем номер
data.Ticket[data.Ticket == ''] = 0 #заменяем отсутствующие номера билетов 0, чтобы не было неопределенности

data.Age[data.Age.isnull()] = 0
data.Fare[data.Fare.isnull()] = 0

itog = data.drop('Name',axis=1)

itog.head()

from sklearn.preprocessing import LabelEncoder
label = LabelEncoder()
dicts = []

label.fit(itog.Sex)
dicts.append({'Sex': list(label.classes_)})
itog.Sex = label.transform(itog.Sex)

label.fit(itog.Cabin.drop_duplicates())
dicts.append({'Cabin': list(label.classes_)})
itog.Cabin = label.transform(itog.Cabin)

label.fit(itog.Embarked.drop_duplicates())
dicts.append({'Embarked': list(label.classes_)})
itog.Embarked = label.transform(itog.Embarked)

label.fit(itog.SrTicket.drop_duplicates())
dicts.append({'SrTicket': list(label.classes_)})
itog.SrTicket = label.transform(itog.SrTicket)


TestResult = read_csv('Kaggle_Titanic/Data/test.csv')
pretest = TestResult
pretest.Cabin = pretest.Cabin.str[0]
pretest.Ticket = pretest.Ticket.str.replace('\.|/','') #убираем лишние символы из серии
pretest.insert(len(pretest.columns),'SrTicket','') #добавляем столбец в котором будет записана серия
pretest.SrTicket = pretest.Ticket.str.replace(' \d*','')
pretest.Ticket = pretest.Ticket.str.replace('\D*','')
pretest.Ticket[pretest.Ticket.isnull()] = 0
pretest.Age[pretest.Age.isnull()] = 0
pretest.Fare[pretest.Fare.isnull()] = 0
pretest = pretest.drop('Name',axis=1)

label.fit(dicts[0]['Sex'])
pretest.Sex = label.transform(pretest.Sex)
label.fit(pretest.Cabin.drop_duplicates())
pretest.Cabin = label.transform(pretest.Cabin)
label.fit(dicts[2]['Embarked'])
pretest.Embarked = label.transform(pretest.Embarked)
label.fit(pretest.SrTicket.drop_duplicates())
pretest.SrTicket = label.transform(pretest.SrTicket)



from sklearn import cross_validation, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
import pylab as pl


target = itog.Survived
train = itog.drop(['Survived','PassengerId'], axis=1) #из исходных данных убираем Id пассажира и флаг спасся он или нет
test = pretest.drop(['PassengerId'], axis=1) #из исходных данных убираем Id пассажира и флаг спасся он или нет
train.Ticket = train.Ticket.astype(int)
test.Ticket = test.Ticket.astype(int)

kfold = 5 #количество подвыборок для валидации
itog_val = {} #список для записи результатов кросс валидации разных алгоритмов

ROCtrainTRN, ROCtestTRN, ROCtrainTRG, ROCtestTRG = cross_validation.train_test_split(train, target, test_size=0.25) 

model_rfc = RandomForestClassifier(n_estimators = 40) #в параметре передаем кол-во деревьев
model_knc = KNeighborsClassifier(n_neighbors = 18) #в параметре передаем кол-во соседей
model_lr = LogisticRegression(penalty='l1', tol=0.01) 
model_svc = svm.SVC() #по умолчанию kernek='rbf'


scores = cross_validation.cross_val_score(model_rfc, train, target, cv = kfold)
itog_val['RandomForestClassifier'] = scores.mean()
scores = cross_validation.cross_val_score(model_knc, train, target, cv = kfold)
itog_val['KNeighborsClassifier'] = scores.mean()
scores = cross_validation.cross_val_score(model_lr, train, target, cv = kfold)
itog_val['LogisticRegression'] = scores.mean()
scores = cross_validation.cross_val_score(model_svc, train, target, cv = kfold)
itog_val['SVC'] = scores.mean()

#рисуем результат
DataFrame.from_dict(data = itog_val, orient='index').plot(kind='bar', legend=False)

pl.clf()
plt.figure(figsize=(8,6))
#SVC
model_svc.probability = True
probas = model_svc.fit(ROCtrainTRN, ROCtrainTRG).predict_proba(ROCtestTRN)
fpr, tpr, thresholds = roc_curve(ROCtestTRG, probas[:, 1])
roc_auc  = auc(fpr, tpr)
pl.plot(fpr, tpr, label='%s ROC (area = %0.2f)' % ('SVC', roc_auc))
#RandomForestClassifier
probas = model_rfc.fit(ROCtrainTRN, ROCtrainTRG).predict_proba(ROCtestTRN)
fpr, tpr, thresholds = roc_curve(ROCtestTRG, probas[:, 1])
roc_auc  = auc(fpr, tpr)
pl.plot(fpr, tpr, label='%s ROC (area = %0.2f)' % ('RandonForest',roc_auc))
#KNeighborsClassifier
probas = model_knc.fit(ROCtrainTRN, ROCtrainTRG).predict_proba(ROCtestTRN)
fpr, tpr, thresholds = roc_curve(ROCtestTRG, probas[:, 1])
roc_auc  = auc(fpr, tpr)
pl.plot(fpr, tpr, label='%s ROC (area = %0.2f)' % ('KNeighborsClassifier',roc_auc))
#LogisticRegression
probas = model_lr.fit(ROCtrainTRN, ROCtrainTRG).predict_proba(ROCtestTRN)
fpr, tpr, thresholds = roc_curve(ROCtestTRG, probas[:, 1])
roc_auc  = auc(fpr, tpr)
pl.plot(fpr, tpr, label='%s ROC (area = %0.2f)' % ('LogisticRegression',roc_auc))
pl.plot([0, 1], [0, 1], 'k--')
pl.xlim([0.0, 1.0])
pl.ylim([0.0, 1.0])
pl.xlabel('False Positive Rate')
pl.ylabel('True Positive Rate')
pl.legend(loc=0, fontsize='small')
pl.show()

model_rfc.fit(train, target)
TestResult.insert(1,'Survived', model_rfc.predict(test))
TestResult[['PassengerId','Survived']].to_csv('Kaggle_Titanic/Result/test.csv', index=False)

