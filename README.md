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
    "user_id":"23423432424234324",
    "connection_name":"temperature Sensing",
    "connection_discription":"temperature Sensing",
    "created_at":"234234324234234",
    "protocol":"mqtt",
    "connection_url":"http://localhost:",
    "port":2344,
    "subscribe_topic":"",
    "qos":4,
    "keep_alive":30,
    "authenticated_broker":false,
    "username":"",
    "password":"",
    "typeof_connection":"online",
    "ping_status":false,
    "response_parameters":[]

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












### Execution
#### Using Docker
```bash
docker build -t iotstudioapi .
docker run -p 5000:5000 --name iotstudioapicontainer iotstudioapi

```

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