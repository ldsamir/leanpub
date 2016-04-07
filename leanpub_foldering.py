# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 18:03:27 2016

@author: smusali
"""

import urllib2, json, os

def get_file(url, filename):
    try:
        fd = urllib2.urlopen(url);
        fw = open(filename, 'w');
        fr = fd.read();
        fw.write(fr);
        fw.close;
        print url + ' ==> ' + filename;
        return 1;
    except:
        return 0;

def get_folder(folder_list):
    try:
        current = os.getcwd();
        for folder in folder_list:
            if (os.path.isdir(folder) == False):
                os.mkdir(folder);
            os.chdir(folder)
        os.chdir(current);
        path = '/'.join(folder_list);
        print path + ' is ready!';
        return path;
    except:
        return 0;
    
with open('BData.json', 'r') as BDataHandler:
     BDataDB = json.load(BDataHandler);
     
#main_folder = raw_input('Enter the main folder name: ');
main_folder = 'Leanpub';
if os.path.isdir(main_folder):
    import shutil;
    shutil.rmtree(main_folder);
os.mkdir(main_folder);
current = os.getcwd();
os.chdir(main_folder);

for book in BDataDB:
    if ('PDF' not in book.keys()):
        continue;
    lang = book['Book Language'];
    if (lang != 'English'):
        continue;
    name = book['Full Book Name'];
    name.replace('/','_slash_');
    link = book['PDF'];
    if ('Full Category' in book.keys()):
        fold = book['Full Category'];
        for folder in fold:
            path = os.getcwd();
            temp = get_folder(folder);
            if (temp):
                path += '/'+temp;
                get_file(link, path+'/'+name+'.pdf');
    else:
        path = os.getcwd();
        get_file(link, path+'/'+name+'.pdf');
        
os.chdir(current);