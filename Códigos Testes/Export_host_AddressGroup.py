#Bibliotecas
import requests
import ssl
import csv
from time import sleep
##################################Ignorar certificado SSL############################################################
from requests.packages.urllib3.exceptions import InsecureRequestWarning
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context 
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
####################################Variáveis Globais###############################################################
session = requests.Session()
base_url = 'https://(#COLOCAR A URL#)/BeyondTrust/api/public/v3'
#####################################Signin#########################################################################
    #variáveis:
header = {'Authorization': 'PS-Auth key=(#COLOCAR A CHAVE DE ACESSO#);runas=(#COLOCAR O USUÁRIO DE ACESSO#);'}
    #Solicitação
session.headers.update(header)
response_connect = session.post(f'{base_url}/Auth/SignAppin', verify=False)
    #Result
if response_connect.status_code >= 200 and response_connect.status_code <= 299:
    print ('Sucessfully')
    print (response_connect.status_code)
else:
    print ('Unsuccessfully')
    print (response_connect.status_code)

#################################################################################################################
h = ("AddressGroup, HostName\n")
with open ("Export_Hosts_AddressGroup.csv", "a+") as file:  
    file.write(h)
response_addressgroup = session.get(f'{base_url}/Addressgroups', verify=False)
for row in response_addressgroup.json():
    address_name = row ['Name']
    address_id =row ['AddressGroupID']
    #Resgatando os hosts cadastrados no AddressGroup:
    response_folder = session.get(f'{base_url}/Addressgroups/{address_id}/addresses', verify=False)
    for row in response_folder.json():
        host_name = row ['Value'] 
        with open ("Export_Hosts_AddressGroup.csv", "+a", encoding="utf-8") as file: 
            file.write(f"{address_name}, {host_name}\n")
##########################################Signout################################################################
response_disconnect = session.post(f'{base_url}/Auth/Signout', verify=False)
print (response_disconnect.status_code)