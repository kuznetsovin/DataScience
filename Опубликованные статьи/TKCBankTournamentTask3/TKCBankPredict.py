# -*- coding: utf-8 -*-

from pandas import read_csv, DataFrame
from sklearn.metrics import roc_curve
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
import ml_metrics, string, re, pylab as pl



SampleCustomers = read_csv("https://static.tcsbank.ru/documents/olymp/SAMPLE_CUSTOMERS.csv", ';')
SampleAccounts = read_csv("https://static.tcsbank.ru/documents/olymp/SAMPLE_ACCOUNTS.csv",";",decimal =',')

SampleCustomers.head()

print "%s from %s" % (SampleAccounts.tcs_customer_id.drop_duplicates().count(), SampleAccounts.tcs_customer_id.count())

SampleAccounts[['tcs_customer_id','open_date','final_pmt_date','credit_limit','currency']].drop_duplicates()

SampleAccounts.final_pmt_date[SampleAccounts.final_pmt_date.isnull()] = SampleAccounts.fact_close_date[SampleAccounts.final_pmt_date.isnull()].astype(float)
SampleAccounts.final_pmt_date.fillna(0, inplace=True)

sumtbl = SampleAccounts.pivot_table(['inf_confirm_date'],
                                    ['tcs_customer_id','open_date','final_pmt_date','credit_limit','currency'], 
                                    aggfunc='max')
sumtbl.head(15)

SampleAccounts = SampleAccounts.merge(sumtbl, 'left', 
                                     left_on=['tcs_customer_id','open_date','final_pmt_date','credit_limit','currency'], 
                                     right_index=True,
                                     suffixes=('', '_max'))


# преобразуем pmt_string_84m
vals = list(xrange(10)) + ['A','X']
PMTstr = DataFrame([{'pmt_string_84m_%s' % (str(j)): str(i).count(str(j)) for j in vals} for i in SampleAccounts.pmt_string_84m])
SampleAccounts = SampleAccounts.join(PMTstr).drop(['pmt_string_84m'], axis=1)

# преобразуем pmt_freq
SampleAccounts.pmt_freq.fillna(7, inplace=True)
SampleAccounts.pmt_freq[SampleAccounts.pmt_freq == 0] = 7
vals = list(range(1,8)) + ['A','B']
PMTstr = DataFrame([{'pmt_freq_%s' % (str(j)): str(i).count(str(j)) for j in vals} for i in SampleAccounts.pmt_freq])
SampleAccounts = SampleAccounts.join(PMTstr).drop(['pmt_freq'], axis=1)

# преобразуем type
vals = [1,4,6,7,9,10,11,12,13,14,99]
PMTstr = DataFrame([{'type_%s' % (str(j)): str(i).count(str(j)) for j in vals} for i in SampleAccounts.type])
SampleAccounts = SampleAccounts.join(PMTstr).drop(['type'], axis=1)

# преобразуем status
vals = [0,12, 13, 14, 21, 52,61]
PMTstr = DataFrame([{'status_%s' % (str(j)): str(i).count(str(j)) for j in vals} for i in SampleAccounts.status])
SampleAccounts = SampleAccounts.join(PMTstr).drop(['status'], axis=1)

# преобразуем relationship
vals = [1,2,4,5,9]
PMTstr = DataFrame([{'relationship_%s' % (str(j)): str(i).count(str(j)) for j in vals} for i in SampleAccounts.relationship])
SampleAccounts = SampleAccounts.join(PMTstr).drop(['relationship'], axis=1)

# преобразуем bureau_cd
vals = [1,2,3]
PMTstr = DataFrame([{'bureau_cd_%s' % (str(j)): str(i).count(str(j)) for j in vals} for i in SampleAccounts.bureau_cd])
SampleAccounts = SampleAccounts.join(PMTstr).drop(['bureau_cd'], axis=1)

SampleAccounts.fact_close_date[SampleAccounts.fact_close_date.notnull()] = 1
SampleAccounts.fact_close_date.fillna(0, inplace=True)

PreFinalDS = SampleAccounts[SampleAccounts.inf_confirm_date == SampleAccounts.inf_confirm_date_max].drop_duplicates()

PreFinalDS = PreFinalDS.groupby(['tcs_customer_id','open_date','final_pmt_date','credit_limit','currency']).max().reset_index()


PreFinalDS = PreFinalDS.drop(['bki_request_date',
                              'inf_confirm_date',
                              'pmt_string_start',
                              'interest_rate',
                              'open_date',
                              'final_pmt_date',
                              'inf_confirm_date_max'], axis=1)


curs = DataFrame([33.13,44.99,36.49,1], index=['USD','EUR','GHF','RUB'], columns=['crs'])
PreFinalDS = PreFinalDS.merge(curs, 'left', left_on='currency', right_index=True)
PreFinalDS.credit_limit = PreFinalDS.credit_limit * PreFinalDS.crs

#выделяем значения в отдельные столбцы
vals = ['RUB','USD','EUR','CHF']
PMTstr = DataFrame([{'currency_%s' % (str(j)): str(i).count(str(j)) for j in vals} for i in PreFinalDS.currency])
PreFinalDS = PreFinalDS.join(PMTstr).drop(['currency','crs'], axis=1)


PreFinalDS['count_credit'] = 1

PreFinalDS.fillna(0, inplace=True)
FinalDF = PreFinalDS.groupby('tcs_customer_id').sum()
FinalDF

SampleCustomers.set_index('tcs_customer_id', inplace=True)
UnionDF = FinalDF.join(SampleCustomers)
trainDF = UnionDF[UnionDF.sample_type == 'train'].drop(['sample_type'], axis=1)
testDF = UnionDF[UnionDF.sample_type == 'test'].drop(['sample_type'], axis=1)

CorrKoef = trainDF.corr()
CorrKoef


FieldDrop = [i for i in CorrKoef if CorrKoef[i].isnull().drop_duplicates().values[0]]
FieldDrop

CorField = []
for i in CorrKoef:
    for j in CorrKoef.index[CorrKoef[i] > 0.9]:
        if i <> j and j not in CorField and i not in CorField:
            CorField.append(j)
            print "%s-->%s: r^2=%f" % (i,j, CorrKoef[i][CorrKoef.index==j].values[0])



FieldDrop =FieldDrop + ['fact_close_date','ttl_delq_30',
                        'pmt_string_84m_5',
                        'pmt_string_84m_A',
                        'pmt_string_84m_A',
                        'max_delq_balance',
                        'relationship_1',
                        'currency_RUB',
                        'count_credit']
newtr = trainDF.drop(FieldDrop, axis=1)

target = newtr.bad.values
train = newtr.drop('bad', axis=1).values

coder = PCA(n_components=20)
train = coder.fit_transform(train)

models = []
models.append(RandomForestClassifier(n_estimators=165, max_depth=4, criterion='entropy'))
models.append(GradientBoostingClassifier(max_depth =4))
models.append(KNeighborsClassifier(n_neighbors=20))
models.append(GaussianNB())

TRNtrain, TRNtest, TARtrain, TARtest = train_test_split(train, target, test_size=0.3, random_state=0)

plt.figure(figsize=(10, 10)) 
for model in models:
    model.fit(TRNtrain, TARtrain)
    pred_scr = model.predict_proba(TRNtest)[:, 1]
    fpr, tpr, thresholds = roc_curve(TARtest, pred_scr)
    roc_auc = ml_metrics.auc(TARtest, pred_scr)
    md = str(model)
    md = md[:md.find('(')]
    pl.plot(fpr, tpr, label='ROC fold %s (auc = %0.2f)' % (md, roc_auc))

pl.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6))
pl.xlim([0, 1])
pl.ylim([0, 1])
pl.xlabel('False Positive Rate')
pl.ylabel('True Positive Rate')
pl.title('Receiver operating characteristic example')
pl.legend(loc="lower right")
pl.show()


#приводим тестовую выборку к нужному формату
FieldDrop.append('bad')
test = testDF.drop(FieldDrop, axis=1).values
test = coder.fit_transform(test)

#обучаем модель
model = models[1]
model.fit(train, target)

#записываем результат
testDF.bad = model.predict(test)