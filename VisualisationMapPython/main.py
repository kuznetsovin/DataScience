# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 11:43:08 2013

@author: IgKuznetsov
"""
import vincent

rus = 'RusMap/russia_1e-7sr.json'
geo_data = [{'name': 'states',
             'url': rus,
             'feature': 'russia'}]

vis = vincent.Map(geo_data=geo_data)
vis.to_json('map.json', html_out=True, html_path='map.html')