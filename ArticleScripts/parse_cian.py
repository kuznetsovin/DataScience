# -*- coding: utf-8 -*-
import lxml.html as html
import re, csv, time
from pandas import DataFrame, read_csv

page = html.parse('http://www.cian.ru/cat.php?deal_type=2&obl_id=1&room1=1&room2=1&room3=1&p=1')
                  #'http://www.cian.ru/cat.php?deal_type=2&obl_id=1&room1=1&room2=1')

main = page.getroot()
tbody = main.get_element_by_id('tbody')
pre_table = tbody.find_class('cat')
table_cat_list = [t for t in pre_table if t.tag == 'table']
table = table_cat_list[0]

def load_table(id_page):
    page = html.parse('http://www.cian.ru/cat.php?deal_type=2&obl_id=1&room1=1&room2=1&room3=1&p=%s' % (id_page))
    main = page.getroot()
    tbody = main.get_element_by_id('tbody')
    pre_table = tbody.find_class('cat')
    table = table_cat_list[0]
    return table

rows = [row for row in table.getchildren() if row.attrib.has_key('class') and row.attrib['class'] == 'cat']

metro_station_list = {u'м.Авиамоторная':1,
u'м.Автозаводская':2,
u'м.Академическая':3,
u'м.Александровский сад':4,
u'м.Алексеевская':5,
u'м.Алтуфьево':6,
u'м.Аннино':7,
u'м.Арбатская':8,
u'м.Аэропорт':9,
u'м.Бабушкинская':10,
u'м.Багратионовская':11,
u'м.Баррикадная':12,
u'м.Бауманская':13,
u'м.Беговая':14,
u'м.Белорусская':15,
u'м.Беляево':16,
u'м.Бибирево':17,
u'м.Библиотека имени Ленина':18,
u'м.Битцевский парк':19,
u'м.Боровицкая':20,
u'м.Ботаническийсад':21,
u'м.Братиславская':22,
u'м.Бульвар адмирала Ушакова':23,
u'м.Бульвар Дмитрия Донского':24,
u'м.Бунинская аллея':25,
u'м.Варшавская':26,
u'м.ВДНХ':27,
u'м.Владыкино':28,
u'м.Водный стадион':29,
u'м.Войковская':30,
u'м.Волгоградский проспект':31,
u'м.Волжская':32,
u'м.Волоколамская':33,
u'м.Воробьевы горы':34,
u'м.Выставочная':35,
u'м.Выхино':36,
u'м.Деловой центр':37,
u'м.Динамо':38,
u'м.Дмитровская':39,
u'м.Добрынинская':40,
u'м.Домодедовская':41,
u'м.Достоевская':42,
u'м.Дубровка':43,
u'м.Жулебино':44,
u'м.Измайловская':45,
u'м.Калужская':46,
u'м.Кантемировская':47,
u'м.Каховская':48,
u'м.Каширская':49,
u'м.Киевская':50,
u'м.Китай-город':51,
u'м.Кожуховская':52,
u'м.Коломенская':53,
u'м.Комсомольская':54,
u'м.Коньково':55,
u'м.Красногвардейская':56,
u'м.Краснопресненская':57,
u'м.Красносельская':58,
u'м.Красные ворота':59,
u'м.Крестьянская застава':60,
u'м.Кропоткинская':61,
u'м.Крылатское':62,
u'м.Кузнецкий мост':63,
u'м.Кузьминки':64,
u'м.Кунцевская':65,
u'м.Курская':66,
u'м.Кутузовская':67,
u'м.Ленинский проспект':68,
u'м.Лубянка':69,
u'м.Люблино':70,
u'м.Марксистская':71,
u'м.Марьина роща':72,
u'м.Марьино':73,
u'м.Маяковская':74,
u'м.Медведково':75,
u'м.Международная':76,
u'м.Менделеевская':77,
u'м.Митино':78,
u'м.Молодежная':79,
u'м.Мякинино':80,
u'м.Нагатинская':81,
u'м.Нагорная':82,
u'м.Нахимовский проспект':83,
u'м.Новогиреево':84,
u'м.Новокузнецкая':85,
u'м.Новослободская':86,
u'м.Новоясеневская':87,
u'м.Новые Черемушки':88,
u'м.Октябрьская':89,
u'м.Октябрьское поле':90,
u'м.Орехово':91,
u'м.Отрадное':92,
u'м.Охотный ряд':93,
u'м.Павелецкая':94,
u'м.Парк культуры':95,
u'м.Парк Победы':96,
u'м.Партизанская':97,
u'м.Первомайская':98,
u'м.Перово':99,
u'м.Петровско-Разумовская':100,
u'м.Печатники':101,
u'м.Пионерская':102,
u'м.Планерная':103,
u'м.Площадь Ильича':104,
u'м.Площадь Революции':105,
u'м.Полежаевская':106,
u'м.Полянка':107,
u'м.Пражская':108,
u'м.Преображенская площадь':109,
u'м.Пролетарская':110,
u'м.Проспект Вернадского':111,
u'м.ПроспектМира':112,
u'м.Профсоюзная':113,
u'м.Пушкинская':114,
u'м.Речнойвокзал':115,
u'м.Рижская':116,
u'м.Римская':117,
u'м.Рязанский проспект':118,
u'м.Савеловская':119,
u'м.Свиблово':120,
u'м.Севастопольская':121,
u'м.Семеновская':122,
u'м.Серпуховская':123,
u'м.Славянский бульвар':124,
u'м.Смоленская':125,
u'м.Сокол':126,
u'м.Сокольники':127,
u'м.Спортивная':128,
u'м.Сретенский бульвар':129,
u'м.Строгино':130,
u'м.Студенческая':131,
u'м.Сухаревская':132,
u'м.Сходненская':133,
u'м.Таганская':134,
u'м.Тверская':135,
u'м.Театральная':136,
u'м.Текстильщики':137,
u'м.ТеплыйСтан':138,
u'м.Тимирязевская':139,
u'м.Третьяковская':140,
u'м.Трубная':141,
u'м.Тульская':142,
u'м.Тургеневская':143,
u'м.Тушинская':144,
u'м.Улица 1905 года':145,
u'м.Улица Академика Янгеля':146,
u'м.Улица Горчакова':147,
u'м.Улица Подбельского':148,
u'м.Улица Скобелевская':149,
u'м.Улица Старокачаловская':150,
u'м.Университет':151,
u'м.Филевский парк':152,
u'м.Фили':153,
u'м.Фрунзенская':154,
u'м.Царицыно':155,
u'м.Цветной бульвар':156,
u'м.Черкизовская':157,
u'м.Чертановская':158,
u'м.Чеховская':159,
u'м.Чистые пруды':160,
u'м.Чкаловская':161,
u'м.Шаболовская':162,
u'м.Шоссе Энтузиастов':163,
u'м.Щелковская':164,
u'м.Щукинская':165,
u'м.Электрозаводская':166,
u'м.Юго-Западная':167,
u'м.Южная':168,
u'м.Ясенево':169}

square = {u'общая':'all_sqr', 
          u'жилая':'room_sqr', 
          u'кухня':'kitchen_sqr'
          }

dop_des = {u'Лифт':'lift', 
           u'Балкон':'balkon', 
           u'Окна':'windows', 
           u'Санузел':'tolet', 
           u'Телефон':'tel'
           }

typ = [u'Новостройка', u'Вторичка']

material_desc = {u'пан':u'панельный дом',
                 u'стал':u'сталинский',
                 u'кирп':u'кирпичный',
                 u'мон':u'монолитный',
                 u'к-м':u'кирпично-монолитный',
                 u'блоч':u'блочный',
                 u'дер':u'деревянный'}

def row_parse(row):
    res = {}
    for i in row.getchildren():
        if i.attrib.has_key('id'):
            field =  re.sub(r"\w*_", "", i.attrib['id'])
            if field == 'metro':
                for j in i.itertext(): 
                    if j in metro_station_list: 
                        res['metro'] = metro_station_list[j]
                    else:
                        res['metro'] = nan
            elif field == 'room':
                if i.text_content().find(u'-комн. квартира') > -1:
                    res['room_count'] = int(i.text_content().replace(u'-комн. квартира',''))
                else:
                    res['room_count'] = i.text_content()
            elif field == 'rooms':
                for sqr_type in i.itertext():  
                    tmp = sqr_type.split(':')
                    if tmp[0] in square:
                        res[square[tmp[0]]] = float(re.sub(u"м2|м", "", tmp[1]))
            elif field == 'price':
                prices = prices = [int(re.sub(r"\D*", "", price_val)) for price_val in i.itertext() if len(price_val) > 1]
                res['price_rur'] = prices[0]
                res['price_usd'] = prices[1]
            elif field == 'floor':
                floor = [flr.split('/')  for flr in i.itertext()]           
                res['floor_flat'] = floor[0][0]
                res['floor_all'] = floor[0][1]
                res['material_desc'] = material_desc[floor[1][0]]
            elif field == 'dopsved':
                for param in i.itertext():
                    if param.find(';') == -1:
                        tmp = param.split(':')
                        if tmp[0] in dop_des:
                            res[dop_des[tmp[0]]] = tmp[1].strip()
                        elif tmp[0] in typ:
                            res['typ'] = tmp[0]
                    else:
                        for split_param in param.split('; '):
                            tmp = split_param.split(':')
                            res[dop_des[tmp[0]]] = tmp[1].strip()
    return res

parse_list = [row_parse(tr) for tr in rows]
df = DataFrame(parse_list)

parse_list = []
for page_num in range(1,2500):
    load_table(page_num)
    rows = [row for row in table.getchildren() if row.attrib.has_key('class') and row.attrib['class'] == 'cat']
    for tr in rows: parse_list.append(row_parse(tr))
    # для обманки сервера
    if page_num % 100:
        time.sleep(60)
    else:
        time.sleep(120)
        
df = DataFrame(parse_list)
df.to_csv('DataSets\parse_flat_all.csv',';',index=False, encoding='utf-8')

df.balkon[df.balkon == u'нет'] = 0
df.balkon.drop_duplicates()



