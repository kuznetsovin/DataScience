# -*- coding: utf-8 -*-
import lxml.html as html
import re, csv, time
from pandas import DataFrame, read_csv

page = html.parse('http://www.banki.ru/products/deposits/search/Moskva/?PAGEN_1=1&filter=0&sort_param=undefined&sort_order=undefined&PAGESIZE=25&sum=100+000&currency=45&period=6&capitalization=2&replenishment=2&withdrawable=2&SPECIAL_DEPOSIT%5B1%5D=2&SPECIAL_DEPOSIT%5B2%5D=0&SPECIAL_DEPOSIT%5B7%5D=2&SPECIAL_DEPOSIT%5B4%5D=2&SPECIAL_DEPOSIT%5B5%5D=0&SPECIAL_DEPOSIT%5B6%5D=2&SPECIAL_DEPOSIT%5B3%5D=2&SPECIAL_DEPOSIT%5B10%5D=0&SPECIAL_DEPOSIT%5B8%5D=2&bankShow=all&bankTop=50&match=%2Fproducts%2Fdeposits%2Fsearch%2FMoskva%2F%3Ffilter%3D0&regionInfo=Moskva#nav_start')

main = page.getroot()
div_table = main.find_class('b-deposits').pop()
table = div_table.find_class('t-page').pop()
rows = [row for row in table.getchildren()]

def load_url(URL):
    page = html.parse(URL)
    main = page.getroot()
    div_table = main.find_class('b-deposits').pop()
    table = div_table.find_class('t-page').pop()
    rows = [row for row in table.getchildren()]
    return rows

def get_bank_rating(url):
    bank = html.parse(url)
    rating_table = bank.getroot().body\
                    .find_class('wrapper wrapper--background-white wrapper--border-grey').pop()\
                    .find_class('l-c-column').pop()\
                    .find_class('widget-gray-panel').pop()\
                    .find_class('b-kb-creditRating').pop()\
                    .find_class('b-kb-2col__right').pop()\
                    .get_element_by_id('creditRatingsTables')\
                    .find_class('b-kb-cRatings__table').pop(0)
    rec = {}
    for row in rating_table:
        agency = row.find_class('b-kb-cRatings__agency-link').pop().text.strip()
        rating = row.find_class('b-kb-cRatings__value').pop().text.strip()
        rec[agency] = rating
    return rec

def parse_record(record):
    res = {}
    for field in record.getchildren():   
        if field.tag == 'td':
            if field.attrib['class'] == 't-page__sorted':
                a =  field.find_class('b-deposits-item').pop()
                info = [k.text_content().strip() for k in a.getchildren()]
                res['dep_name'] = info[0]
                res['bank'] = info[1]
                href = field.find_class('b-deposits-item__bank').pop()\
                        .getchildren().pop()\
                        .attrib['href']
                url = 'http://www.banki.ru%s' % (href)
                #print url
                res.update(get_bank_rating(url))
            elif field.attrib['class'] == 't-page__options':
                spec_deposit = field.find_class('b-deposit-about_special').pop().text_content()
                res['spec_deposit'] = int(spec_deposit.strip() <> '')
                option = field.find_class('b-deposit-about').pop()
                for opt in option:                    
                    res[opt.attrib['class'][41:]] = 1 
            elif field.attrib['class'] == 't-page__rate':
                res['rate'] = float(field.text.replace(',','.').replace('%',''))
            elif field.attrib['class'].strip() == 't-page__amount':
                res['min_amount'] =  int(re.sub('\D*', '', field.text))
            elif field.attrib['class'] == 't-page__term':
                div_term = field.getchildren().pop()
                res['day_term'] = int(re.sub('\D*', '',div_term.attrib['title']))
            elif field.attrib['class'] == 't-page__profit':
                res['profit'] = int(re.sub('\D*', '', field.text_content().strip()))
    return res

for i in res.iteritems():
    print i[0],i[1]

URL = [
       'http://www.banki.ru/products/deposits/search/Moskva/?PAGEN_1=1&filter=0&sort_param=undefined&sort_order=undefined&PAGESIZE=25&sum=100+000&currency=45&period=6&capitalization=2&replenishment=2&withdrawable=2&SPECIAL_DEPOSIT%5B1%5D=2&SPECIAL_DEPOSIT%5B2%5D=0&SPECIAL_DEPOSIT%5B7%5D=2&SPECIAL_DEPOSIT%5B4%5D=2&SPECIAL_DEPOSIT%5B5%5D=0&SPECIAL_DEPOSIT%5B6%5D=2&SPECIAL_DEPOSIT%5B3%5D=2&SPECIAL_DEPOSIT%5B10%5D=0&SPECIAL_DEPOSIT%5B8%5D=2&bankShow=all&bankTop=50&match=%2Fproducts%2Fdeposits%2Fsearch%2FMoskva%2F%3Ffilter%3D0&regionInfo=Moskva#nav_start',
       'http://www.banki.ru/products/deposits/search/Moskva/?PAGEN_1=2&filter=0&sort_param=undefined&sort_order=undefined&PAGESIZE=25&sum=100+000&currency=45&period=6&capitalization=2&replenishment=2&withdrawable=2&SPECIAL_DEPOSIT%5B1%5D=2&SPECIAL_DEPOSIT%5B2%5D=0&SPECIAL_DEPOSIT%5B7%5D=2&SPECIAL_DEPOSIT%5B4%5D=2&SPECIAL_DEPOSIT%5B5%5D=0&SPECIAL_DEPOSIT%5B6%5D=2&SPECIAL_DEPOSIT%5B3%5D=2&SPECIAL_DEPOSIT%5B10%5D=0&SPECIAL_DEPOSIT%5B8%5D=2&bankShow=all&bankTop=50&match=%2Fproducts%2Fdeposits%2Fsearch%2FMoskva%2F%3Ffilter%3D0&regionInfo=Moskva#nav_start',
       'http://www.banki.ru/products/deposits/search/Moskva/?PAGEN_1=3&filter=0&sort_param=undefined&sort_order=undefined&PAGESIZE=25&sum=100+000&currency=45&period=6&capitalization=2&replenishment=2&withdrawable=2&SPECIAL_DEPOSIT%5B1%5D=2&SPECIAL_DEPOSIT%5B2%5D=0&SPECIAL_DEPOSIT%5B7%5D=2&SPECIAL_DEPOSIT%5B4%5D=2&SPECIAL_DEPOSIT%5B5%5D=0&SPECIAL_DEPOSIT%5B6%5D=2&SPECIAL_DEPOSIT%5B3%5D=2&SPECIAL_DEPOSIT%5B10%5D=0&SPECIAL_DEPOSIT%5B8%5D=2&bankShow=all&bankTop=50&match=%2Fproducts%2Fdeposits%2Fsearch%2FMoskva%2F%3Ffilter%3D0&regionInfo=Moskva#nav_start',
       'http://www.banki.ru/products/deposits/search/Moskva/?PAGEN_1=4&filter=0&sort_param=undefined&sort_order=undefined&PAGESIZE=25&sum=100+000&currency=45&period=6&capitalization=2&replenishment=2&withdrawable=2&SPECIAL_DEPOSIT%5B1%5D=2&SPECIAL_DEPOSIT%5B2%5D=0&SPECIAL_DEPOSIT%5B7%5D=2&SPECIAL_DEPOSIT%5B4%5D=2&SPECIAL_DEPOSIT%5B5%5D=0&SPECIAL_DEPOSIT%5B6%5D=2&SPECIAL_DEPOSIT%5B3%5D=2&SPECIAL_DEPOSIT%5B10%5D=0&SPECIAL_DEPOSIT%5B8%5D=2&bankShow=all&bankTop=50&match=%2Fproducts%2Fdeposits%2Fsearch%2FMoskva%2F%3Ffilter%3D0&regionInfo=Moskva#nav_start',
       'http://www.banki.ru/products/deposits/search/Moskva/?PAGEN_1=5&filter=0&sort_param=undefined&sort_order=undefined&PAGESIZE=25&sum=100+000&currency=45&period=6&capitalization=2&replenishment=2&withdrawable=2&SPECIAL_DEPOSIT%5B1%5D=2&SPECIAL_DEPOSIT%5B2%5D=0&SPECIAL_DEPOSIT%5B7%5D=2&SPECIAL_DEPOSIT%5B4%5D=2&SPECIAL_DEPOSIT%5B5%5D=0&SPECIAL_DEPOSIT%5B6%5D=2&SPECIAL_DEPOSIT%5B3%5D=2&SPECIAL_DEPOSIT%5B10%5D=0&SPECIAL_DEPOSIT%5B8%5D=2&bankShow=all&bankTop=50&match=%2Fproducts%2Fdeposits%2Fsearch%2FMoskva%2F%3Ffilter%3D0&regionInfo=Moskva#nav_start',
       'http://www.banki.ru/products/deposits/search/Moskva/?PAGEN_1=6&filter=0&sort_param=undefined&sort_order=undefined&PAGESIZE=25&sum=100+000&currency=45&period=6&capitalization=2&replenishment=2&withdrawable=2&SPECIAL_DEPOSIT%5B1%5D=2&SPECIAL_DEPOSIT%5B2%5D=0&SPECIAL_DEPOSIT%5B7%5D=2&SPECIAL_DEPOSIT%5B4%5D=2&SPECIAL_DEPOSIT%5B5%5D=0&SPECIAL_DEPOSIT%5B6%5D=2&SPECIAL_DEPOSIT%5B3%5D=2&SPECIAL_DEPOSIT%5B10%5D=0&SPECIAL_DEPOSIT%5B8%5D=2&bankShow=all&bankTop=50&match=%2Fproducts%2Fdeposits%2Fsearch%2FMoskva%2F%3Ffilter%3D0&regionInfo=Moskva#nav_start',
       'http://www.banki.ru/products/deposits/search/Moskva/?PAGEN_1=7&filter=0&sort_param=undefined&sort_order=undefined&PAGESIZE=25&sum=100+000&currency=45&period=6&capitalization=2&replenishment=2&withdrawable=2&SPECIAL_DEPOSIT%5B1%5D=2&SPECIAL_DEPOSIT%5B2%5D=0&SPECIAL_DEPOSIT%5B7%5D=2&SPECIAL_DEPOSIT%5B4%5D=2&SPECIAL_DEPOSIT%5B5%5D=0&SPECIAL_DEPOSIT%5B6%5D=2&SPECIAL_DEPOSIT%5B3%5D=2&SPECIAL_DEPOSIT%5B10%5D=0&SPECIAL_DEPOSIT%5B8%5D=2&bankShow=all&bankTop=50&match=%2Fproducts%2Fdeposits%2Fsearch%2FMoskva%2F%3Ffilter%3D0&regionInfo=Moskva#nav_start',
       'http://www.banki.ru/products/deposits/search/Moskva/?PAGEN_1=8&filter=0&sort_param=undefined&sort_order=undefined&PAGESIZE=25&sum=100+000&currency=45&period=6&capitalization=2&replenishment=2&withdrawable=2&SPECIAL_DEPOSIT%5B1%5D=2&SPECIAL_DEPOSIT%5B2%5D=0&SPECIAL_DEPOSIT%5B7%5D=2&SPECIAL_DEPOSIT%5B4%5D=2&SPECIAL_DEPOSIT%5B5%5D=0&SPECIAL_DEPOSIT%5B6%5D=2&SPECIAL_DEPOSIT%5B3%5D=2&SPECIAL_DEPOSIT%5B10%5D=0&SPECIAL_DEPOSIT%5B8%5D=2&bankShow=all&bankTop=50&match=%2Fproducts%2Fdeposits%2Fsearch%2FMoskva%2F%3Ffilter%3D0&regionInfo=Moskva#nav_start']

itog = []
for adr in URL:    
    for rec in rws: itog.append(parse_record(rec))
    time.sleep(180)
df = DataFrame(itog)
df.to_csv('DataSets\parse_deposit.csv',';',index=False, encoding='utf-8')