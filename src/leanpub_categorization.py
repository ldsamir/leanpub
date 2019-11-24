from bs4 import BeautifulSoup
import urllib2, json, os

def get_soup(url, header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))

def split_path(path):
    lpath = path.split('/');
    return map(lambda x: x.rstrip().lstrip(), lpath);
    
with open('BData.json', 'r') as BDataHandler:
     BDataDB = json.load(BDataHandler);
     
booknames = map(lambda x: x['Short Book Name'], BDataDB);
header = {'User-Agent': 'Mozilla/5.0'}
base_urls = 'https://leanpub.com/bookstore/earnings_in_last_7_days/';
main_urls = 'all/all/1';
main_soup = get_soup(base_urls+main_urls, header);
main_part = main_soup.find_all('ul', {'class': 'menu has-default flush-right'})[0].find_all('div', {'class': 'scrollable'})[0].find_all('li')[1:];
path_data = map(lambda x: (x.find('a')['data-nav-path'], split_path(x.find('a').contents[0])), main_part)
for path in path_data:
    CUR = 1;
    old_names = list();
    while (True):
        url = base_urls+path[0]+'/all/'+str(CUR);
        try:
            soup = get_soup(url, header);
            print '\n'+str(CUR)+' of '+path[0]+'\n';
        except:
            break;
        items = soup.find_all('div', {'class': 'book-list-item'});
        if (len(items) == 0):
            break;
        names = map(lambda x: x.find('a')['href'][1:], items);
        if (names == old_names):
            break;
        for name in names:
            if (name in booknames):
                if ('Short Category Name' not in BDataDB[booknames.index(name)].keys()):
                    BDataDB[booknames.index(name)]['Short Category Name'] = [path[0]];
                    BDataDB[booknames.index(name)]['Full Category'] = [path[1]];
                else:
                    if (path[0] not in BDataDB[booknames.index(name)]['Short Category Name']):
                        BDataDB[booknames.index(name)]['Short Category Name'].append(path[0]);
                    if (path[1] not in BDataDB[booknames.index(name)]['Full Category']):
                        if (len(path[1]) > 1 and path[1][:-1] in BDataDB[booknames.index(name)]['Full Category']):
                            BDataDB[booknames.index(name)]['Full Category'].remove(path[1][:-1]);
                        BDataDB[booknames.index(name)]['Full Category'].append(path[1]);
                import pprint
                pprint.pprint(BDataDB[booknames.index(name)]);
        CUR += 1;
        old_names = names;

if (os.path.exists('BData.json')):
    os.remove('BData.json');
        
with open('BData.json', 'w') as BDataHandler:
    json.dump(BDataDB, BDataHandler);