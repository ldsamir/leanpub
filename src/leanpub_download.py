# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 17:17:34 2016

@author: smusali
"""

from bs4 import BeautifulSoup
import urllib2, json

def get_soup(url, header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))

header = {'User-Agent': 'Mozilla/5.0'}
leanpub_gmail = BeautifulSoup(open('leanpub_gmail.html'));
leanpub_table = leanpub_gmail.find_all('table', {'style': "border-collapse:collapse;border-spacing:0;width:100%;margin-bottom:12px", 'cellpadding': "0", 'cellspacing': "0", 'width': "100"});
leanpub_ppart = map(lambda x: x.find('p', {'style': 'margin:0'}), leanpub_table);
leanpub_tbody = map(lambda x: x.find('table').find('tbody'), leanpub_table);
MAX_BOOKS = len(leanpub_ppart);
leanpub_books = list();
for i in xrange(MAX_BOOKS):
    ppart = leanpub_ppart[i];
    tbody = leanpub_tbody[i];
    dlink = tbody.find_all('a', {'style': "outline:none;color:#009aff;text-decoration:none"});
    dbook = dict();
    atags = ppart.find_all('a');
    blink = atags[0]['href'];
    bsoup = get_soup(blink, header);
    blang = bsoup.find_all('li', {'class': 'detail language'})[0].find_all('p')[0].contents[0];
    alink = atags[1:];
    aname = list();
    asnam = list();
    for author in alink:
        abuff = author['href'];
        asnam.append(abuff[abuff.find('/u/')+3:]);
        if (str(author).find('@') != -1):
            asnam.append(author.contents[0]);
        try:
            asoup = get_soup(author['href'], header);
            atemp = asoup.find_all('h3', {'class': 'profile-name'})[0].contents[0];
            atemp = (atemp[1:])[:-1];
            aname.append(atemp);
        except:
            aname.append(author.contents[0]);
    sname = blink[blink.find('.com/')+5:];
    bname = atags[0].contents[0];
    dbook['Short Book Name'] = sname;
    dbook['Full Book Name'] = bname;
    dbook['Short Author Names'] = ', '.join(asnam);
    dbook['Book Link'] = blink;
    dbook['Author Links'] = ', '.join(map(lambda x: x['href'], alink));
    dbook['Book Language'] = (blang[1:])[:-1];
    dbook['Full Author Names'] = ', '.join(aname);
    for download in dlink:
        dbook[download.contents[0]] = download['href'];
    print "Book No."+str(i+1)+":";
    keys = dbook.keys();
    for key in keys:
        print " "+key+": "+dbook[key];
    leanpub_books.append(dbook);
    
with open('BData.json', 'w') as BDataFileHandler:
    json.dump(leanpub_books, BDataFileHandler);