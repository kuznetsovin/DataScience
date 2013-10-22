# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 11:43:08 2013

@author: IgKuznetsov
"""
import vincent

world_topo = r'TestWorldMap/world-countries.topo.json'
geo_data = [{'name': 'countries',
             'url': world_topo,
             'feature': 'world-countries'}]

vis = vincent.Map(geo_data=geo_data, scale=200)
vis.to_json('map.json', html_out=True, html_path='map.html')
