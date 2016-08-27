#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import re
import csv

main_site = 'http://www.umniylogist.ru{}'


def get_company_contacts(company_url, output=None):
    print "Parse company page: {}".format(company_url)
    
    url = main_site.format(company_url)
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "lxml")

    company = dict()
    name_node = soup.find_all('span', class_='fn org')
    company['name'] = name_node[0].string if len(name_node) > 0 else ""

    address_node = soup.find_all('td', class_='adr street-address')
    company['address'] = address_node[0].string if len(address_node) > 0 else ""

    phone_node = soup.find_all('td', class_='tel')
    company['phone'] = phone_node[0].string if len(phone_node) > 0 else ""

    email_node = soup.find_all('td', class_='email')
    company['email'] = email_node[0].string if len(email_node) > 0 else ""

    for k, v in company.items():
        company[k] = v.encode('utf-8') if v is not None else ""

    output.writerow(company)
    print "Company info save in file"
    return company


if __name__ == "__main__":
    print "Creating output file..."
    f = open('umniylogist.csv', 'w')
    result = csv.DictWriter(f, delimiter=";", fieldnames=['name', 'address', 'phone', 'email'])
    result.writeheader()

    page = urllib2.urlopen(main_site.format("/company")).read()
    soup = BeautifulSoup(page, "lxml")

    print "Get company links..."
    table_companes = soup.find_all('a', href=re.compile("/company/\d+"))

    map(lambda x: get_company_contacts(x.get('href'), result), table_companes)

    print "Saving data file..."
    f.close()

    print "Data was saved"
