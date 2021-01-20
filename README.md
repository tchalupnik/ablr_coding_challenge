ABLR Coding Challenge 2020
==========================

## Overview

Use the existing code provided (or roll your own as you see fit), build a **Django-backend** application with
**React frontend** to demonstrate the integration with MyInfo APIs, similar to the Demo app provided by 
Singapore Government Technology Agency (GovTech): https://github.com/ndi-trusted-data/myinfo-demo-app


## Evaluation Criteria

We will look at your project and assess it for:

1. Extensibility - separation of concerns.
2. Simplicity - aim for the simplest solution that gets the job done whilst remaining
readable, extensible and testable.
3. Test Coverage - breaking changes should break your tests.
4. Robustness - should handle and report errors.
If you have any questions about this criteria please ask.

## Specifications

### With docker
1. Prerequisites: docker, docker-compose
2. Create `.env` with variables:
    - `MYINFO_ROOT`
    - `MYINFO_CLIENT_ID` 
    - `MYINFO_SECRET`
2. Run `docker-compose up`
3. Go on `localhost:3000`

### Without docker
1. Prerequisites: python, pip, node, npm
2. Create `.env` with variables (and source this file):
    - `MYINFO_ROOT`
    - `MYINFO_CLIENT_ID` 
    - `MYINFO_SECRET`
3. Run 2 consoles
4. On first console: 
    ```
    cd backend
    pip install -r requirements.txt
    python manage.py runserver
    ```
5. On second console:
    ```
    cd frontend
    npm install
    npm start
    ```
6. Go on `localhost:3000`

### Run tests
1. First two steps the same as in `Run without docker`
2. In console:
    ```
    cd backend
    pip install -r requirements.txt
    pytest
    ```

## Submission

Github is the preferred option (a public repo is fine) but we will also accept a .zip file if
necessary. Email your solution to team@ablr.com.


## MyInfo Python API Usage

Set up virtualenv

```shell script
python3 -m venv env
pip install -r requirements.txt
```

In python shell

```python
from myinfo.client import MyInfoClient
from myinfo.security import get_decoded_access_token, get_decrypted_person_data

client = MyInfoClient()
client.get_authorise_url(state="blahblah")
# Open up this SingPass Authorise URL and follow instructions
# After clicking on the green "I Agree" button, you'll be redirected back to
# http://localhost:3001/callback?code=25e3a9679bfc9baca7ef47bceadea43fcd6eb199&state=blahblah
# Then grab the code for the next API call

# Getting access token with code
code = "25e3a9679bfc9baca7ef47bceadea43fcd6eb199"
resp = client.get_access_token(code)
access_token = resp["access_token"]

# Decoding access token
decoded_access_token = get_decoded_access_token(access_token)
uinfin = decoded_access_token["sub"]

# Getting person data
resp = client.get_person(uinfin=uinfin, access_token=access_token)
decrypted = get_decrypted_person_data(resp)
print(decrypted)
```

### Sample work

* Contact Info

![Contact Info](./sample/contact_info.png)

* Personal Info

![Personal Info](./sample/personal_info.png)

* Income Info

![Income Info](./sample/income_info.png)
