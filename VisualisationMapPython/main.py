# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 11:43:08 2013

@author: IgKuznetsov
"""
import vincent
vincent.core.initialize_notebook()

world_topo = r'world-countries.topo.json'
geo_data = [{'name': 'countries',
             'url': world_topo,
             'feature': 'world-countries'}]

vis = vincent.Map(geo_data=geo_data, scale=200)
vis.display()