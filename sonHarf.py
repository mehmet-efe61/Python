import sys

while True:
    str = str(input("Adın Ne?\n"))
    
    if str.endswith("a"):
        print(str+"'nın  Bilgisayarı")

    elif str.endswith("e"):
        print(str+"'nin  Bilgisayarı")

    elif str.endswith("i"):
        print(str+"'nin  Bilgisayarı")

    elif str.endswith("ı"):
        print(str+"'nın  Bilgisayarı")

    elif str.endswith("o"):
        print(str+"'nun  Bilgisayarı")

    elif str.endswith("ö"):
        print(str+"'nün  Bilgisayarı")

    elif str.endswith("u"):
        print(str+"'nun  Bilgisayarı")

    elif str.endswith("ü"):
        print(str+"'nün  Bilgisayarı")
        
    elif str.endswith("b"):
        print(str+"'in  Bilgisayarı")
    
    elif str.endswith("c"):
        print(str+"'ın  Bilgisayarı")
    
    elif str.endswith("d"):
        print(str+"'nin  Bilgisayarı")
    
    elif str.endswith("af"):
        print(str+"'ın  Bilgisayarı")
    
    else:
        print("Geçersiz bir ad yazdınız. Tekrar Deneyin")
