
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
# Ongoing Refactor tasks
1. Move orm files inside database & common to model & schema 
2. Restructuring class

## TODO
- ValidationErrors
- cascade delete records
- *failsafe* function to catch generic success and raise
- move apis to routers/
- add proper schema (roles)
- look for auto documentations
- install docker desktop
- pytest? (TDD)

## Quick Lookup
### SQL
- Declarative Mapping -> to further tune sql datatypes
- CTE - common table expression to simplify complex queries
- windowed function (operation over group of row instead of whole table) - *RANK*
- Loader Strategies -> see them when needed

### FastAPI
- there's enum
- https://app.quicktype.io/
- path as Annotated + Query for validation  + ?regex
- Annotated + Type + Depends `commons: Annotated[CommonQueryParams, Depends()]`
- ... is required
- add metadata to Query coz, they'll be part of openAPI
- additional metadata, such as data validation, descriptions, default values -> PATH


## Quick Explainations
### SQL
- backpopulate - keep python classes in consistent state (back & forth in a relationship)
    - ^^ commit insert of parent first, then the next class in relation
- only during flush, orm communicates with sql - autoflushed before select statement -> session.dirty True/False
- rollback()

### FastAPI
- path operation order matters
- Depends - manages lifecycle by itself
