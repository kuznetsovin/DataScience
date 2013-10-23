# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 11:43:08 2013

@author: IgKuznetsov
"""
#import vincent
#rus = 'RusMap/russia.json'
#geo_data = [{'name': 'states',
#             'url': rus,
#             'feature': 'russia'}]
#
#vis = vincent.Map(geo_data=geo_data, scale=700, projection='conicEqualArea', rotate = [-105,0], center = [-10, 65])
#vis.to_json('example_map.json', html_out=True, html_path='example_map.html')

import pandas as pd
import requests


url = u'http://ru.wikipedia.org/wiki/Список_городов_России'
City = pd.read_html(
    requests.get(url,headers={'User-agent': 'Mozilla/5.0'}).text, 
    header=0, 
    attrs = {'class':'wikitable sortable'})[0]
CityRegion = City[[u'Регион',u'Город']]
CityRegion.rename(columns={u'Регион':'region',u'Город':'city_name'}, inplace=True)
CityRegion.region = CityRegion.region.str.replace(u'авт. окр.',u'автономный округ')
spr = pd.read_csv('RusMap/russia-region-names.tsv','\t',header=None, names = ['region','code'], encoding='utf-8')
spr.region = spr.region.str.replace(u'Республика ','')
spr.region = spr.region.str.replace(u'Город ','')
a = CityRegion.merge(spr, 'left', 'region')