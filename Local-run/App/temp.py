import os

 
# get current directory
path = os.getcwd()
print("Current Directory", path)
print()
 
# parent directory
parent = os.path.dirname(os.path.dirname(__file__))
print("Parent directory", parent)


with open(parent+"/ipaddress.txt", "r+") as ipaddress_file:
    ip_address = ipaddress_file.read()     # Reading form a file

print(ip_address)
