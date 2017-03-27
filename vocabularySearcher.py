import time
import webbrowser
import sys
while True:
    a=str(input("Kelimeyi girin\n"))
    if a  == "exit":
        sys.exit()
    else:
        for i in range(4):
            print("Loading" + "." * i)
            sys.stdout.write("\033[F")
            time.sleep(.200)
        webbrowser.open("http://dictionary.cambridge.org/dictionary/turkish/"+a)
        webbrowser.open("http://www.thesaurus.com/browse/"+a+"?s=t")
        webbrowser.open("http://zargan.com/tr/q/"+a+"-ceviri-nedir")
