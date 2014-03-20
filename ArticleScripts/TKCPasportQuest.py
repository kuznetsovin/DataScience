# -*- coding: utf-8 -*-

from pandas import read_csv
import pymorphy2
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.decomposition import PCA

train = read_csv('https://static.tcsbank.ru/documents/olymp/passport_training_set.csv',';', index_col='id' ,encoding='cp1251')

train.head(5)

example_code = train.passport_div_code[train.passport_div_code.duplicated()].values[0]
for i in train.passport_issuer_name[train.passport_div_code == example_code].drop_duplicates():
    print i

train.passport_issuer_name = train.passport_issuer_name.str.lower()
train[train.passport_div_code == example_code].head(5)

train.passport_issuer_name = train.passport_issuer_name.str.replace(u'р-(а|й|о|н|е)*',u'район')
train.passport_issuer_name = train.passport_issuer_name.str.replace(u' г( |\.|(ор(\.| )))', u' город ')
train.passport_issuer_name = train.passport_issuer_name.str.replace(u' р(\.|есп )', u' республика ')
train.passport_issuer_name = train.passport_issuer_name.str.replace(u' адм([а-я]*)(\.)?', u' административный ')
train.passport_issuer_name = train.passport_issuer_name.str.replace(u' окр(\.| |уга( )?)', u' округ ')
train.passport_issuer_name = train.passport_issuer_name.str.replace(u' ао ', u' административный округ ')

train.passport_issuer_name = train.passport_issuer_name.str.replace(u' - ?', u'-')
train.passport_issuer_name = train.passport_issuer_name.str.replace(u'[^а-я -]','')
train.passport_issuer_name = train.passport_issuer_name.str.replace(u'- ',' ')
train.passport_issuer_name = train.passport_issuer_name.str.replace(u'  *',' ')

sokr = {u'нао': u'ненецкий автономный округ',
u'хмао': u'ханты-мансийский автономный округ',
u'чао': u'чукотский автономный округ',
u'янао': u'ямало-ненецкий автономный округ',
u'вао': u'восточный административный округ',
u'цао': u'центральный административный округ',
u'зао': u'западный административный округ',
u'cао': u'северный административный округ',
u'юао': u'южный административный округ',
u'юзао': u'юго-западный округ',
u'ювао': u'юго-восточный округ',
u'свао': u'северо-восточный округ',
u'сзао': u'северо-западный округ',
u'оуфмс': u'отдел управление федеральной миграционной службы',
u'офмс': u'отдел федеральной миграционной службы',
u'уфмс': u'управление федеральной миграционной службы',
u'увд': u'управление внутренних дел',
u'ровд': u'районный отдел внутренних дел',
u'говд': u'городской отдел внутренних дел',
u'рувд': u'районное управление внутренних дел',
u'овд': u'отдел внутренних дел',
u'оувд': u'отдел управления внутренних дел',
u'мро': u'межрайонный отдел',
u'пс': u'паспортный стол',
u'тп': u'территориальный пункт'}

for i in sokr.iterkeys():
    train.passport_issuer_name = train.passport_issuer_name.str.replace(u'( %s )|(^%s)|(%s$)' % (i,i,i), u' %s ' % (sokr[i]))
    
train.passport_issuer_name = train.passport_issuer_name.str.lstrip()
train.passport_issuer_name = train.passport_issuer_name.str.rstrip()

train = train.drop(['passport_issue_month/year'], axis=1)

def f_tokenizer(s):
    morph = pymorphy2.MorphAnalyzer()
    if type(s) == unicode:
        t = s.split(' ')
    else:
        t = s
    f = []
    for j in t:
        m = morph.parse(j.replace('.',''))
        if len(m) <> 0:
            wrd = m[0]
            if wrd.tag.POS not in ('NUMR','PREP','CONJ','PRCL','INTJ'):
                f.append(wrd.normal_form)
    return f

coder = HashingVectorizer(tokenizer=f_tokenizer, encoding='KOI8-R', n_features=256)

TrainNotDuble = train.drop_duplicates()
trn = coder.fit_transform(TrainNotDuble.passport_issuer_name.tolist()).toarray()

target = TrainNotDuble.passport_div_code.values

pca = PCA(n_components = 15)
trn = pca.fit_transform(trn)

model = RandomForestClassifier(n_estimators = 100, criterion='entropy')

TRNtrain, TRNtest, TARtrain, TARtest = train_test_split(trn, target, test_size=0.4)
model.fit(TRNtrain, TARtrain)
print 'accuracy_score: ', accuracy_score(TARtest, model.predict(TRNtest))

