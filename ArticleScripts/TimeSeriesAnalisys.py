# -*- coding: utf-8 -*-
from pandas import read_csv, DataFrame
import statsmodels.api as sm
from statsmodels.iolib.table import SimpleTable
from sklearn.metrics import r2_score
import ml_metrics as metrics

dataset = read_csv('tovar_moving.csv',';', index_col=['date_oper'], parse_dates=['date_oper'], dayfirst=True)
dataset.head()

otg = dataset.Otgruzka

otg.plot(figsize=(12,6))

otg = otg.resample('W', how='mean')
otg.plot(figsize=(12,6))

itog = otg.describe()
otg.hist()

print 'V = %f' % (itog['std']/itog['mean'])

row =  [u'JB', u'p-value', u'skew', u'kurtosis']
jb_test = sm.stats.stattools.jarque_bera(otg)
a = np.vstack([jb_test])
itog = SimpleTable(a, row)
print itog

otg1diff = otg.diff(periods=1).dropna()

test = sm.tsa.adfuller(otg1diff)
print 'adf: ', test[0]
print 'p-value: ', test[1]
print'Critical values: ', test[4]
if test[0]> test[4]['5%']: 
    print 'есть единичные корни, ряд не стационарен'
else:
    print 'единичных корней нет, ряд стационарен'

m = otg1diff.index[len(otg1diff.index)/2+1]
r1 = sm.stats.DescrStatsW(otg1diff[m:])
r2 = sm.stats.DescrStatsW(otg1diff[:m])
print 'p-value: ', sm.stats.CompareMeans(r1,r2).ttest_ind()[1]

otg1diff.plot(figsize=(12,6))

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(otg1diff.values.squeeze(), lags=25, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(otg1diff, lags=25, ax=ax2)
src_data_model = otg[:'2013-05-26']
model = sm.tsa.ARIMA(src_data_model, order=(1,1,1), freq='W').fit(full_output=False, disp=0)

print model.summary()

q_test = sm.tsa.stattools.acf(model.resid, qstat=True) #свойство resid, хранит остатки модели 
                                                            #qstat=True, означает что применяем указынный тест к коэф-ам
print DataFrame({'Q-stat':q_test[1], 'p-value':q_test[2]})

pred = model.predict('2013-05-26','2014-12-31', typ='levels')
trn = otg['2013-05-26':]

r2 = r2_score(trn, pred[1:32])
print 'R^2: %1.2f' % r2

metrics.rmse(trn,pred[1:32])
metrics.mae(trn,pred[1:32])

otg.plot(figsize=(12,6))
pred.plot(style='r--')