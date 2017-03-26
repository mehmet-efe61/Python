import time
import os
import sys

def loading():
    for i in range(4):
        print("Loading" + "." * i)
        sys.stdout.write("\033[F")
        time.sleep(.500)

print("Adın ne?")
if str(input()) == "Alper":
    loading()
    print("\nGit burdan, oç!")
    sys.exit()

elif str(input()) == "Efe":
    loading()
    print("\nAccess Granted")
    sys.exit()
else:
    loading()
    print("\nAferin")
    sys.exit()

os.system("say 'hello world'")
