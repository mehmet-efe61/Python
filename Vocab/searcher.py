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

word=str(input("Enter the word\n"))
os.system("say "+word+" -v daniel")

url="http://dictionary.cambridge.org/dictionary/english/"+word
page=urllib.request.urlopen(url)
soup=BeautifulSoup(page,"html.parser")
print("Definition: "+(soup.find('b',{"class":"def"}).text).strip())

url="http://dictionary.cambridge.org/dictionary/turkish/"+word
page=urllib.request.urlopen(url)
soup=BeautifulSoup(page,"html.parser")
print("Example: "+(soup.find('div',{"class":"examp emphasized"}).text).strip())

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
