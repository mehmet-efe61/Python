import time
import webbrowser
import sys
import urllib
import urllib.request
from bs4 import BeautifulSoup
import os

def translate():
    url="http://dictionary.cambridge.org/dictionary/english-"+lang+"/"+word
    page=urllib.request.urlopen(url)
    soup=BeautifulSoup(page,"html.parser")
    print(lang+": "+(soup.find('span',{"class":"trans"}).text).strip())
    print(" ")

while True:
    word=str(input("Enter the word\n"))
    os.system("say "+word+" -v daniel")

    url="https://www.ldoceonline.com/dictionary/"+word
    page=urllib.request.urlopen(url)
    soup=BeautifulSoup(page,"html.parser")
    print("Part of Speech: "+(soup.find('span',{"class":"POS"}).text).strip())
    print(" ")
    print("Definition: "+(soup.find('span',{"class":"DEF"}).text).strip())
    print(" ")

    try:
        url="http://dictionary.cambridge.org/dictionary/turkish/"+word
        page=urllib.request.urlopen(url)
        soup=BeautifulSoup(page,"html.parser")
        print("Example: "+(soup.find('div',{"class":"examp emphasized"}).text).strip())
        print(" ")
    except:
        url="http://dictionary.cambridge.org/dictionary/english/"+word
        page=urllib.request.urlopen(url)
        soup=BeautifulSoup(page,"html.parser")
        print("Example: "+(soup.find('div',{"class":"examp emphasized"}).text).strip())
        print(" ")

    lang="turkish"
    url="http://dictionary.cambridge.org/dictionary/"+lang+"/"+word
    page=urllib.request.urlopen(url)
    soup=BeautifulSoup(page,"html.parser")
    print(lang+": "+(soup.find('span',{"class":"trans"}).text).strip())
    print(" ")

    lang="german"
    translate()

    lang="spanish"
    translate()

    lang="french"
    translate()
