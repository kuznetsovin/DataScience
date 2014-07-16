# coding: utf-8

import urllib2, re
from bs4 import BeautifulSoup
from pandas import DataFrame

def load_data(pages_num):
    parse_list = []
    
    for num in pages_num:
        site = urllib2.urlopen('http://www.realto.ru/base/flat_sale/?SecLodg_step=%s' % num)
        page = BeautifulSoup(site)
        info_table = page.find('table', class_ = 'table_base')    

        for row in info_table.find_all('tr', class_ = 'row_base'):
            lst = row.find_all('td')
            sqr = re.findall(r'\d+', lst[4].text)
            level, level_sum = re.findall(r'\d+', lst[5].text)

            rec = {
                'price' : int(''.join(re.findall(r'\d+', lst[0].small.text))),
                'reg' : lst[1].text.strip(),
                'loc' : [loc.strip() for loc in lst[2].strings][0].strip(),
                'rooms' : int(re.findall(r'\d+', lst[3].text)[0]),
                'sum_sqr' : int(sqr[0]) if len(sqr) >= 1 else 0,
                'live_sqr' : int(sqr[1]) if len(sqr) >= 2 else 0,
                'kit_sqr' : int(sqr[2]) if len(sqr) >= 3 else 0,
                'level' : int(level),
                'level_sum' : int(level_sum),
                'tp' : ''.join(re.findall(r'[^\d+|/]', lst[5].text)).strip()
            }
            parse_list.append(rec)    
    return DataFrame(parse_list)