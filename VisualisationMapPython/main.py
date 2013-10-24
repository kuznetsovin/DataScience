# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 11:43:08 2013

@author: IgKuznetsov
"""

import pandas as pd

#загружаем статистику регионов и справочник с кодами регионов используемыми в карте
stat = pd.read_html('Data/AVGPeopleProfit.htm', header=0, index_col=0)[0]
spr = pd.read_csv('Data/russia-region-names.tsv','\t', index_col=0, header=None, names = ['name','code'], encoding='utf-8')
#приводим имена ригеонов в стат данных к справочному виду и обновляем индекс
new_index = stat.index.to_series().str.replace(u'(2\))|(1\))|(г. )','')
stat.set_index(new_index, inplace=True)
#добавляем к стат данным коды регионов для построения карты
RegionProfit = stat.join(spr, how='inner')
#удяляем лишние неинформаивные столбцы
RegionProfit.drop([1990], axis=1)

import vincent
#подключаем карту d3
geo_data = [{'name': 'rus',
             'url': 'RusMap/russia.json',
             'feature': 'russia'}]
#отрисовываем карту с привязкой стат данных по регионмам
vis = vincent.Map(data=RegionProfit, geo_data=geo_data,scale=700, projection='conicEqualArea', rotate = [-105,0], center = [-10, 65],
          data_bind=2011, data_key='code',
          map_key={'rus': 'properties.region'})
#задаем полупрозрачные границы регионов
vis.marks[0].properties.enter.stroke_opacity = vincent.ValueRef(value=0.5)
#задаем градацию по цвету для группы для отображения на карте
vis.scales['color'].type = 'threshold'
vis.scales['color'].domain = [0, 10000, 15000, 20000, 25000, 30000]
#вводим название легенды карты
vis.legend(title=u'Доходы руб.')
#выгружаем итоговую карту
vis.to_json('example_map.json', html_out=True, html_path='example_map.html')
