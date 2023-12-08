
# Student Management

## Overview of commands
```bash
virtualenv venv
.\venv\Scripts\activate
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
cd app
uvicorn main:router --reload
```

Just incase
```bash
pip install virtualenv
```

## TODO
- use pydantic
- Schema
- base settings?
- ValidationErrors
- look for auto documentations
- install postgres 
- install docker desktop
- pytest? (TDD)