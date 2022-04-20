from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/') 
db = client.C2 

def registerAgent(agentID, agentIP, timeout=86400): 
    
    agent = {   'id': agentID,  
                'timeout': timeout, 
                'ip': agentIP,      
                'task': '',  
                'status': '', 
                'taskResult': ''   }

    db.agents.insert_one(agent)  


def getAgents(): 
    return db.agents.find()


def deleteAgent(agentID): 
    db.agents.delete_one({'id': { '$eq': agentID } })


def saveListener(listenerId, port): 
    listener = {  'id': listenerId, 
                  'port': port      }                   
    db.listeners.insert_one(listener) 


def getListener(id): 
    return db.listeners.find_one({ 'id': { '$eq': id } })


def getListeners(): 
    return db.listeners.find()


def delListener(id): 
    if(db.listeners.delete_one({ 'id' : { '$eq': id } })):
        return True
    else: 
        return False

def checkTask(agentID): 
    task = db.agents.find_one( {'id': {'$eq': agentID} }).get('task') 
    
    if (task): 
        return task 
    
    else: 
        return '0'


def clearTask(agentID): 
        db.agents.update_one({
        'id': agentID 
    },{
        '$set': { 
            'task': ''
        }
    })


def assignTask(agentID, task): 
    
    db.agents.update_one({
        'id': agentID 
    },{
        '$set': { 
            'task': task
        }
    })

def writeResult(agentID, result): 
    db.agents.update_one({
        'id': agentID },
        {
        '$set': { 
            'taskResult': ''
        }
    }) 

