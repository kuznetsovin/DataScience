# -*- coding: utf-8 -*-
"""
Created on Wed Nov 06 12:58:09 2013

@author: IgKuznetsov
"""

from pandas import read_csv

transact = read_csv('transactions.csv',';')
merch = read_csv('merchants.csv',';')
mcc = read_csv('mcc_codes.csv',',', index_col=0)
asw = read_csv('Template_1.csv',';')

mcc_trn = transact[['merchant_type','Merchant_id']].set_index('merchant_type').drop_duplicates()

client_div = mcc_trn.join(mcc)[['Merchant_id','Combined Description']]
client_div.drop_duplicates(inplace=True)
now = client_div.merge(asw, on='Merchant_id')

now = now[now['Merchant Name'].isnull()]