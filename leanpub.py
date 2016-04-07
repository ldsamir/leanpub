from bs4 import BeautifulSoup
import urllib2, json

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))
    
header = {'User-Agent': 'Mozilla/5.0'} 
BLinkDB = dict();

base_link = "https://leanpub.com";
MAX__PAGE = 29;
list_link = "/bookstore/earnings_in_last_7_days/all/all/";
for i in xrange(MAX__PAGE):
    page__num = i+1;
    page_link = base_link+list_link+str(i);
    try:
        page_soup = get_soup(page_link, header);
    except:
        continue;
    page__img = page_soup.find_all('img');
    for img in page__img:
        src = img['src'];
        srt = src.find('b.com')+5;
        end = src.find('/large?');
        book_path = src[srt:end];
        book_link = base_link + book_path;
        try:
            book_soup = get_soup(book_link, header);
        except:
            continue;
        book_span = book_soup.find_all('span');
        for span in book_span:
            book__div = span.find_all('div');
            if (len(book__div) > 0):
                book_dict = book__div[0].attrs;
                if ('data-react-props' in book_dict.keys()):
                    book__drp = book_dict['data-react-props'];
                    if (book__drp.find('FREE') != -1):
                        if (book_link not in BLinkDB.values()):
                            print book_path[1:] + ' is free!';
                            BLinkDB[book_path[1:]] = book_link;

with open('BLink.json', 'w') as BLinkFileHandler:
    json.dump(BLinkDB, BLinkFileHandler);