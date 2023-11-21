import requests
import json


# Ignore Warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Variaveis de ambiente BT
apikey = "XXXXXXXXX"
apiuser = "XXXXXX"
ServidorCofre = "1.1.1.1"
auth_head = 'PS-Auth key={}; runas={};'.format(apikey, apiuser)
base = 'https://{}/BeyondTrust/api/public/v3'.format(ServidorCofre)
header = {'Authorization': auth_head}
datype = {'Content-type': 'application/json'}
session = requests.Session()
session.headers.update(header)
workgroupName = "BEYONDTRUST WORKGROUP";


def sing_in_BT():
    # Signing in
    Signin_url = base + '/Auth/SignAppin'
    print("Signing in...")
    print("#########################################")
    signin = session.post(url=Signin_url, verify=False)  # Sign in
    print ('Signing in HTTP Response Code: {}'.format(signin.status_code))
    print("#########################################")


def Get_Account_BT():
    # ManagedAccounts
    print("Getting Managed Account...")
    print("#########################################")
    '''Trocar nome da conta e ativo na linha a seguir'''
    mn_rl = base + '/ManagedAccounts?systemName=servidorXPT&accountName=root'
    resmacc = session.get(mn_rl, verify=False)  # Get a particular Managed Account
    dic_acc = json.loads(resmacc.text)  # converts json to python dictionary
    #print (dic_acc)
    sys_id = dic_acc['SystemId']  # Grab the systemid
    acc_id = dic_acc['AccountId']  # Grab the Account Id

    # Make Request
    req_url = base + '/Requests'
    reqbody = {'SystemId': sys_id, 'AccountId': acc_id, 'Reason': 'Python Sample', 'DurationMinutes': 5,
               'AccessType': 'View'}  # request body
    data = json.dumps(reqbody)  # convert to json data
    print("Making Request...")
    print("#########################################")
    reqres = session.post(req_url, data=data, headers=datype)
    req_id = reqres.text  # Grab Request ID
    #print(req_id)

    # Get Credentials
    cred_url = base + '/Credentials/{}'.format(req_id)
    cred_res = session.get(cred_url, verify=False)
    senha = (cred_res.text)
    #print(senha)

    # Checkin Request
    rel_url = base + '/Requests/{}/Checkin'.format(req_id)  # checkin request url
    relbody = {'Reason': 'Done Python Sample'}
    reldata = json.dumps(relbody)  # convert release_request body to json
    print("Checking-in Request...")
    print("#########################################")
    chkin = session.put(rel_url, data=reldata, headers=datype)
    #print(chkin)  # Checkin request
    senha_tratada=senha.strip('"')
    return senha_tratada


def Integracao():
    senha = Get_Account_BT()
    print(senha)


def sing_out_BT():
    # Sign Out
    signout_url = base + '/Auth/Signout'
    print("#########################################")
    print("Signing out...")
    print("#########################################")
    signout = session.post(signout_url, verify=False)  # Sign out
    print('Signing out HTTP Response Code: {}'.format(signout.status_code))
    print("#########################################")


def main():
    sing_in_BT()
    Integracao()
    sing_out_BT()

main()