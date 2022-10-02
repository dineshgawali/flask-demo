Installatoin: 
    virtulenv: 
        install, create and activate virtulenv
        $ pip install virtualenv
        $ virtualenv -p python3 venv
        $ source venv/bin/activate

    install requirements.txt in environment
        $ pip install -r requirements.txt

    activate environment variable
        $ export FLASK_ENV=development
        $ export FLASK_APP=app

    run project
        $ flask run -p 8080


test project using curl on other terminal
    $ curl http://127.0.0.1:8080/


API: 

1. Login: 
    Request:
        curl -X POST -F 'username=dinesh1' http://127.0.0.1:8080/restapi/login/
    Response:
        {
        "token": "c43e5883-6d99-49f1-abcb-8c78e4da2f69"
        }        


2. cwd: 
    Request:
        curl -H 'Authorization: Bearer c43e5883-6d99-49f1-abcb-8c78e4da2f69' localhost:8080/restapi/cwd/
    Response:
        {
        "cwd": "/home/dinesh/dinesh/flask"
        }


3. ls: 
    Request:
        curl -H 'Authorization: Bearer c43e5883-6d99-49f1-abcb-8c78e4da2f69' localhost:8080/restapi/ls/
    Response:
        {
            "ls": [
                {
                "name": "README.md", 
                "type": "FILE"
                }, 
                {
                "name": ".git", 
                "type": "DIRECTORY"
                }, 
                {
                "name": "app.py", 
                "type": "FILE"
                }
            ]
        }


4. cd: 
    Request:
        curl -H 'Authorization: Bearer c43e5883-6d99-49f1-abcb-8c78e4da2f69' http://127.0.0.1:8080/restapi/cd/?directory=\/home\/dinesh/\dinesh\/
    Success Response:
        {
            "message": "Directory Changed"
        }
    
    Error Response:
        {
            "message": "Changed directory is not exists"
        }


5. Logout: 
    Request:
        curl -H 'Authorization: Bearer c43e5883-6d99-49f1-abcb-8c78e4da2f69' http://127.0.0.1:8080/restapi/logout/
    Response:
        {
            "message": "User Logout"
        }       
