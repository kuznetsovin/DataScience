# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 11:38:54 2013

@author: igorkuznetsov
"""

import vkontakte
from pyvkoauth import auth
import pandas as pd
import time

user_email = 'kuzn_igor@mail.ru'
user_password = 'Cjwctnm'
client_id = 3860348
scope = 162146
response = auth(user_email, user_password, client_id, scope)
vk = vkontakte.API(token=response['access_token'])

usr=[]
a=[]
offset=0
fld = 'sex, bdate, city, country,counters,relation'
for i in xrange(103):
    print i
    l = vk.get('groups.getMembers', gid='fightwear', offset = offset)
    #a = a + l[u'users']
    usr = usr + vk.get('users.get', uids=l[u'users'][:500], fields = fld)
    usr = usr + vk.get('users.get', uids=l[u'users'][500:], fields = fld)
    offset = offset+1000
    time.sleep(0.3)

profiles = pd.DataFrame.from_dict(usr)
#city_list = ','.join(profiles.city.drop_duplicates().dropna())
#country_list = ','.join(profiles.country.drop_duplicates().dropna())
##profiles = pd.read_csv('user_group.csv')
##city_list = str(list(profiles.city.drop_duplicates().dropna())).replace('.0','')
##city_list = city_list[1:len(city_list)-1]
##country_list = str(list(profiles.country.drop_duplicates().dropna())).replace('.0','')
##country_list = country_list[1:len(country_list)-1]
#city = pd.DataFrame.from_dict(vk.get('getCities',cids = city_list))
#country = pd.DataFrame.from_dict(vk.get('getCountries',cids = country_list))
#profiles.to_csv('user_group.csv', index=False)
#city.to_csv('city.csv', index=False)
#country.to_csv('country.csv', index=False)