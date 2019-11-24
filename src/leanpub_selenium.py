# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 13:08:42 2016

@author: smusali
"""

from selenium import webdriver
import json
'''
email = raw_input('Email: ');
password = raw_input('Password: ');
'''
browser = webdriver.Firefox();
'''
browser.get('https://leanpub.com/login');
browser.find_element_by_id('session_email').send_keys(email);
browser.find_element_by_id('session_password').send_keys(password);
browser.find_element_by_name('commit').click();
'''
with open('BLink.json') as BLinkJSON:
    BLink = json.load(BLinkJSON);

Books = BLink.keys();
MAX = len(Books);
CUR = 0;
ERR = 0;

for book in Books:
    book_url = BLink[book];
    browser.get(book_url);
    payment = browser.find_elements_by_id('you_pay_hero')[0];
    browser.execute_script("arguments[0].value = ''", payment);
    payment.send_keys('0');
    CUR += 1;
    if (CUR > MAX):
        print "Overloading... with "+str(ERR);
    try:
        browser.find_element_by_link_text('Add Ebook to Cart').click();
        print str(CUR)+". "+book+" is Done!";
    except:
        Books.append(book);
        print str(CUR)+". "+book+" is not Done!";
        ERR += 1;
        continue;
