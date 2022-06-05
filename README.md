<img src='https://user-images.githubusercontent.com/54769522/170516883-79c40a1f-13ef-423f-a526-af81cad24191.png' height="300"> 


### What is Venom?
Venom is a Command and Control framework used by red team operators to maintain connection with compromised agents under a stealthy and encrypted channel, by providing an interactive web application and easy to use features.

![image](https://user-images.githubusercontent.com/54769522/172016313-50acd1ab-69a2-476b-ba0f-7a4323ef7bea.png)


# Installation 
Make sure to install MongoDB (Debian) 
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add - && 
echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list && 
sudo apt-get update && 
sudo apt-get install -y mongodb-org && 
sudo systemctl start mongod.service
```
Refer to MongoDB installation Guide
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-debian/

Install Venom requirements 
```bash
pip3 install -r requirments.txt 
``` 

# Usage 
Please refer to Venom documentation and usage guide 
https://j0lger.github.io/bloghub/bloghub/venom/
