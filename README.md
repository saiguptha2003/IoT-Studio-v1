# IoT-Studio


### Routes 

#### Authentication
##### /auth/signup
###### POST /auth/signup
```json
{
    "email":"pandurangasaiguptha@gmail.com",
    "username":"pandurangasa1i3",
    "password":"pandusai"

}
```
###### Output
```json
{
    "error": "Email is already registered"
}
```
---
##### /auth/signin
###### POST /auth/signin
```json
{
    "username_or_email":"pandurangasaiguptha@gmail.com",
    "password":"pandusai"
}
```
###### Output
```json
{
    "email": "pandurangasaiguptha@gmail.com",
    "message": "Login successful",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhbmR1cmFuZ2FzYTFpMyIsImV4cCI6MTczNDcxMDg5NiwidXNlcmlkIjoiYjdmMGNmYzg0MDEzNDMxNWJlNDQ2MWM0MDNiMmQyYjQiLCJlbWFpbCI6InBhbmR1cmFuZ2FzYWlndXB0aGFAZ21haWwuY29tIn0.z-mbWIWhECWBwWolRjmaTezEJtxhknX0oNwqZkig730",
    "user_id": "b7f0cfc840134315be4461c403b2d2b4"
}
```
---

##### /auth/users
###### GET /auth/users
###### Response
```json
[
    {
        "email": "pandurangasaiguptha@gmail.com",
        "id": 1,
        "unique_id": "b7f0cfc840134315be4461c403b2d2b4",
        "username": "pandurangasa1i3"
    }
]
```

---

##### services/IoTConnect/createConnection
###### POST services/IoTConnect/createConnection
```json
{
    "connection_name":"temperaturef Sensing",
    "connection_discription":"temperature Sensing",
    "created_at":"234234324234234",
    "protocol":"mqtt",
    "connection_url":"http://localhost:",
    "port":2344,
    "subscribe_topic":"fdsafsaf",
    "qos":4,
    "keep_alive":30,
    "authenticated_broker":false,
    "username":"sdfasdf",
    "password":"asdfasdf",
    "typeof_connection":"online",
    "ping_status":false,
    "response_parameters":["fdsf"]

}
```
###### Output
```json
{
    "IoTConnect": [
        {
            "authenticated_broker": false,
            "connection_discription": "temperature Sensing",
            "connection_id": "6912d6f3-69b2-4bc6-85e6-179bc6b880ba",
            "connection_name": "tempedfraturef Sensing",
            "connection_url": "http://localhost:",
            "created_at": "1734883999.782658",
            "keep_alive": 30,
            "password": "asdfasdf",
            "ping_status": false,
            "port": 2344,
            "protocol": "mqtt",
            "qos": 4,
            "response_parameters": [
                "fdsf"
            ],
            "subscribe_topic": "fdsafsaf",
            "typeof_connection": "online",
            "username": "sdfasdf"
        }
    ],
    "connection_id": "6912d6f3-69b2-4bc6-85e6-179bc6b880ba",
    "message": "Service connection created successfully."
}

```

---

##### services/IotConnect/getAllIoTConnections
###### GET services/IotConnect/getAllIoTConnections
###### Output
```json
[
    {
        "authenticated_broker": false,
        "connection_discription": "temperature Sensing",
        "connection_id": "c94cf6a0-bd0f-41ac-84c2-de652b49e828",
        "connection_name": "temperaturef Sensing",
        "connection_url": "http://localhost:",
        "created_at": "1734870244",
        "keep_alive": 30,
        "password": "asdfasdf",
        "ping_status": false,
        "port": 2344,
        "protocol": "mqtt",
        "qos": 4,
        "response_parameters": [
            "fdsf"
        ],
        "subscribe_topic": "fdsafsaf",
        "typeof_connection": "online",
        "username": "sdfasdf"
    }
]
```

---

##### /services/IotConnect/getConnectionById/c94cf6a0-bd0f-41ac-84c2-de652b49e828
###### GET /services/IotConnect/getConnectionById/c94cf6a0-bd0f-41ac-84c2-de652b49e828
###### Output
```json
{
    "authenticated_broker": false,
    "connection_discription": "temperature Sensing",
    "connection_id": "c94cf6a0-bd0f-41ac-84c2-de652b49e828",
    "connection_name": "temperaturef Sensing",
    "connection_url": "http://localhost:",
    "created_at": "1734870244",
    "keep_alive": 30,
    "password": "asdfasdf",
    "ping_status": false,
    "port": 2344,
    "protocol": "mqtt",
    "qos": 4,
    "response_parameters": [
        "fdsf"
    ],
    "subscribe_topic": "fdsafsaf",
    "typeof_connection": "online",
    "username": "sdfasdf"
}
```

---

##### /services/SecureStore/createSecureId
###### POST /services/SecureStore/createSecureId
```json
{
    "secureid_name": "exfamfple3",
    "description": "SomeSecureData",
    "type_of_id":"int"

}
```
###### Output
```json
{
    "entry": {
        "created_at": "1734882554.956195",
        "description": "SomeSecureData",
        "id": "61662747666350133329740576175571615237",
        "secure_id": "51256439772831697251234016972863129176",
        "secureid_name": "exfamfple3",
        "type_of_id": "int"
    },
    "message": "Secure ID created successfully.",
    "secure_id": 51256439772831697251234016972863129176
}
```
---

##### /services/SecureStore/getSecureID/61662747666350133329740576175571615237
###### GET /services/SecureStore/getSecureID/61662747666350133329740576175571615237
###### Output
```json
{
    "created_at": "1734882554.956195",
    "description": "SomeSecureData",
    "id": "61662747666350133329740576175571615237",
    "secure_id": "51256439772831697251234016972863129176",
    "secureid_name": "exfamfple3",
    "type_of_id": "int"
}
```

---

##### /services/SecureStore/getAllSecureIDs
###### GET /services/SecureStore/getAllSecureIDs
###### Output
```json
[
    {
        "created_at": "1734882552.427893",
        "description": "SomeSecureData",
        "id": "157324394069647903541355341246261895017",
        "secure_id": "67690395155127999342968975347141986458",
        "secureid_name": "examfple3",
        "type_of_id": "int"
    }
]
```


---

##### /services/SecureStore/deleteSecureID/61662747666350133329740576175571615237
###### DELETE /services/SecureStore/deleteSecureID/61662747666350133329740576175571615237
###### Output
```json
{
    "deleted_id": "61662747666350133329740576175571615237",
    "message": "Secure ID with id '61662747666350133329740576175571615237' deleted successfully."
}
```

### Execution
#### Using Docker
```bash
docker build -t iotstudioapi .
docker run -p 5000:5000 --name iotstudioapicontainer iotstudioapi

```
#### Docker Compose
to turn on the container 
```bash
docker-compose up -d  # detach after composing the container

```
to turn off the container
```bash
docker-compose down
```
to rebuild application with latest update
```bash
docker-compose up --build -d
#### Using CLI
```bash
pip install -r requirements.txt
python main.py
```


## Connections

### DATABASE URL : https://couchdb-xfm8.onrender.com/_utils
### API URL : https://iot-studio.onrender.com



## Pending Functions

#### creating the requried session time input in frontend and backen in login screen and login route in api