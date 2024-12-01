## INTRODUCTION
This repository contains the API code developed using python and fastapi. The service allows users to upload files to the cloud and uses a failover method in order to abstract the user from the implementation.
It stores the data into a local postgresql instance and uses jwt authentication for every request to the file system.

## TECHNOLOGIES
The project uses:
* <b>python</b> version: 3.11.5
* <b>fastapi</b>: Web framework.
* <b>docker</b>: Container that holds the API.

For a detailed view of the used libraries see 'requirements.txt'

## HOW TO USE
In order to run this project you must install docker in your host machine.

#### 1. Create the '.env' file with all the necesary variables

#### 2. Run the app with the following command:

```
docker-compose up --build
```