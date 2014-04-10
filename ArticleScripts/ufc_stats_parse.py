# coding: utf-8
import lxml.html as html
from pandas import DataFrame, read_csv

main_domain_stat = 'http://hosteddb.fightmetric.com'
page = html.parse('%s/events/index/date/desc/1/all' % (main_domain_stat))
e = page.getroot().find_class('events_table data_table row_is_link').pop()
t = e.getchildren().pop()

events_tabl = DataFrame([{'EVENT':i[0].text, 'LINK':i[2]} for i in t.iterlinks()][5:])
event_date = DataFrame([{'EVENT': evt.getchildren()[0].text_content(), 'DATE':evt.getchildren()[1].text_content()} for evt in t][2:])

sum_event_link = events_tabl.set_index('EVENT').join(event_date.set_index('EVENT')).reset_index()

sum_event_link.to_csv('..\DataSets\ufc\list_ufc_events.csv',';',index=False)

sum_event_link = read_csv('..\DataSets\ufc\list_ufc_events.csv',';')

all_fights = []
for event in sum_event_link.itertuples():
    print event[0], event[1], event[2]
    page_event = html.parse('%s/%s' % (main_domain_stat,event[2]))
    main_code = page_event.getroot()
    figth_event_tbl = main_code.find_class('data_table row_is_link').pop()[1:]
    for figther_num in xrange(len(figth_event_tbl)): 
        if not figther_num % 2:
            all_fights.append(
                    {'FIGHTER_WIN': figth_event_tbl[figther_num][2].text_content().lstrip().rstrip(), 
                    'FIGHTER_LOSE': figth_event_tbl[figther_num+1][1].text_content().lstrip().rstrip(), 
                    'METHOD': figth_event_tbl[figther_num][8].text_content().lstrip().rstrip(), 
                    'METHOD_DESC': figth_event_tbl[figther_num+1][7].text_content().lstrip().rstrip(), 
                    'ROUND': figth_event_tbl[figther_num][9].text_content().lstrip().rstrip(), 
                    'TIME': figth_event_tbl[figther_num][10].text_content().lstrip().rstrip(),
                    'EVENT_NAME':event[1]} 
                    )
history_stat = DataFrame(all_fights)
history_stat.to_csv('..\DataSets\ufc\list_all_fights.csv',';',index=False)

all_statistics = history_stat.set_index('EVENT_NAME').join(sum_event_link.set_index('EVENT').DATE)
all_statistics.to_csv('..\DataSets\ufc\statistics_ufc.csv',';', index_label='EVENT')

