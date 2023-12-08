
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
- add values to db
- ValidationErrors
- JWT - use proper salting
- *failsafe* function to catch generic success and raise
- Alembic migration
- add proper schema (roles)
- change email type
- version numbers on requirements.txt
- look for auto documentations
- install docker desktop
- pytest? (TDD)