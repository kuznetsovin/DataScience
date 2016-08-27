#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lxml.html as html
import csv


main_site = 'http://alliance-catalog.ru'


def get_company_links(page, output_file):
    print "Parse page number {}".format(page)

    url = '{}/gruzoperevozki/moskva/?page={}'.format(main_site, page)
    page = html.parse(url).getroot()
    page_company_links = page.xpath("//div[@class='pad']/a")

    return map(lambda x: get_company_contacts(x, output_file), page_company_links)


def get_company_contacts(link_node, output_file):
    company_link = link_node.attrib['href']
    print "Parse company by link: {}".format(company_link)

    url = '{}{}'.format(main_site, company_link)
    page = html.parse(url).getroot()

    company = dict()
    company_name_node = page.xpath("//div[@class='headline']/div/h1")
    company['name'] = extract_node_text(company_name_node[0]) if len(company_name_node) > 0 else ''

    company_address_node = page.xpath("//div[@class='iconBox geo']/div")
    company['address'] = extract_node_text(company_address_node[0]) if len(company_address_node) > 0 else ''

    company_tel_node = page.xpath("//div[@class='iconBox call']/div")
    company['phone'] = extract_node_text(company_tel_node[0]) if len(company_tel_node) > 0 else ''

    company_contact_nodes = page.xpath("//div[@class='iconBox message']")
    email_node = map(lambda y: filter(lambda x: '@' in x.text_content(), y), company_contact_nodes)
    company['email'] = extract_node_text(email_node[0][0]) if len(email_node[0]) > 0 else ''

    for k, v in company.items():
        company[k] = v.encode('utf-8')

    output_file.writerow(company)
    print "Company info save in file"
    return company


def extract_node_text(node):
    return node.text_content().lstrip().rstrip()


if __name__ == "__main__":
    print "Creating output file..."
    f = open('alliance-catalog.csv', 'w')
    result = csv.DictWriter(f, delimiter=";", fieldnames=['name', 'address', 'phone', 'email'])
    result.writeheader()

    map(lambda x: get_company_links(x, result), range(1, 51))

    print "Saving data file..."
    f.close()

    print "Data was saved"
