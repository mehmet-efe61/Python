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

word=str(input("Kelimeyi girin\n"))
os.system("say "+word+" -v daniel")

lang="turkish"
url="http://dictionary.cambridge.org/dictionary/"+lang+"/"+word
page=urllib.request.urlopen(url)
soup=BeautifulSoup(page,"html.parser")
print(lang+": "+(soup.find('span',{"class":"trans"}).text).strip())

lang="german"
translate()

lang="spanish"
translate()

lang="french"
translate()
