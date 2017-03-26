avrg=((int(input("Birinci notunuz kaçtır?\n"))+int(input("İkinci notunuz kaçtır?\n"))+int(input("Üçüncü notunuz kaçtır?\n")))/3)
if avrg<=100 and 90<=avrg:
    print("AA")
elif avrg<90 and 80<=avrg:
    print("BB")
elif avrg<80 and 70<=avrg:
    print("CC")
elif avrg<70 and 60<=avrg:
    print("DD")
else:
    print("Üzgünüm kaldınız! :(")
