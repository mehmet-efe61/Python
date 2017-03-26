name=str(input("Kullanıcı Adını Gir:\n"))
password=str(input("Şifreni Gir:\n"))

if name=="efe" and password=="12345678":
    print("Login Granted")
elif name=="Efe" and password=="12345678":
    print("Login Granted")
elif name=="EFE" and password=="12345678":
    print("Login Granted")
else:
    print("Access Denied")
