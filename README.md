# Student Management
A simple project that demostrates CRUD using postgres and FastAPI. Containerized in docker, scaled with kubernetes.

## 1. Postgres installation
1. Download latest postgres on your system
2. Enter your username (or postgres by default), a password
3. Open pgAdmin 4 from the start menu
4. No need to create any databases. SQLAlchemy does that for us

---
## 2. Python setup 
1. create a virtual environment, activate it.
2. go to the folder containing 'requirements.txt' and run 
3. cd to **backend/app** folder
4. run the uvicorn command to start the server

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd backend/app
uvicorn main:router --reload
```
Just in case of errors (in windows)
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
---
## 3. Docker setup
1. Install wsl in widows os (the backend for the docker)
2. Install [docker desktop](https://www.docker.com/products/docker-desktop/) and restart the pc
3. Login with an account in docker desktop if necessary 

```bash
wsl --install
```
## 4. Docker image creation
1. check for config files and create respective .env files referring the sample env file
2. build an image using Dockerfile
3. run the basic Dockerfile inside the **backend** folder 
4. use postman to ping at the endpoint

```bash
# (the dot indicates the current folder where Dockerfile is present)
docker build -t mini-school:0.0.3 .
docker images
docker run -d --name mini-school-run-03 -p 80:80 mini-school:0.0.3
```
### Diagnostics commands
```bash
docker login 
docker images
docker ps
docker stop container-name
docker rmi image-name

```
---
## Docker compose (optional)
1. go to the folder containing 'docker-compose.yaml'
2. **don't forget to put your own values on env / config files**
3. run the compose file (has fastapi + postgres image mapping)

note: you can mention the path of the Dockerfile or the name of the image file in docker compose
~~note2: if you want to really understand how dockerfiles work, delete the Dockerfile and write your own from scratch 😊~~

```bash
docker compose -up build -p 80:80
```
---
## 5. Minikube setup
1. Follow the [official instructions](https://minikube.sigs.k8s.io/docs/start/) to install minikube
2. Start the server
3. Make minikube to use local docker context (so that it can access the local docker images)
4. Switch to default namespace (or create your own)
5. Create configmap from .env file
6. pull the database and backend images manually using minikube from local docker environment
7. Apply deployments and services (pods / deloyments / services will autostart the moment you apply them)
8. Portmap to access the running pods from the host machine (so our postman)

```bash
docker context ls
docker use default
minikube start
minikube docker-env
minikube image load postgres:0.0.1
minikube image load mini-school:0.0.3
kubectl create configmap db-configmap --from-env-file .\.env
kubectl apply -f .\backend\k8-backend.yaml
kubectl apply -f .\database\k8-database.yaml
port-forward service/mini-school-be-service 80:80
```
### Diagnostics commands
```bash
kubectl describe configmaps db-configmap
minikube service mini-school-db-service
minikube service mini-school-be-service
kubectl get deployments
kubectl get pods
kubectl get events
kubectl get services
kubectl logs -f mini-school-db-deployment-6cf854ccd4-62wgz
kubectl exec -it mini-school-be-deployment-58bc45cf8d-245m7 bash
kubectl describe pod mini-school-db-deployment-6cf854ccd4-8ppbd
kubectl edit deploy mini-school-db-deployment
```
---

## Quick Explainations
### SQL
- backpopulate - keep python classes in consistent state (back & forth in a relationship)
- ^^ commit insert of parent first, then the next class in relation
- only during flush, orm communicates with sql - autoflushed before select statement -> session.dirty True/False
- rollback()

### FastAPI
- path operation order matters (your endpoints)
- Depends - manages lifecycle by itself

## Nice Findings
### SQL
- try Declarative Mapping -> to further tune sql datatypes (ORM thingy)
- CTE - common table expression to simplify complex queries
- windowed function (operation over group of row instead of whole table) - *RANK*
- Loader Strategies -> see them when needed

### FastAPI
- there's enum
- use https://app.quicktype.io/
- path as Annotated + Query for validation  + ?regex
- Annotated + Type + Depends `commons: Annotated[CommonQueryParams, Depends()]`
- ... is required
- add metadata to Query coz, they'll be part of openAPI
- additional metadata, such as data validation, descriptions, default values -> PATH

## Helpful tools maybe
- [k8 yaml generator](https://gimlet.io/k8s-yaml-generator)
- phind.com 

## Tips
- skim through FastAPI docs
- use url/openapi.json and import it to postman directly
- use service.namespace instead of localhost in FastAPI python app configs when deploying images as pods in k8 cluster
- use base project generator using cookiecutter 
- check best practices [like this](https://github.com/zhanymkanov/fastapi-best-practices) or smth similar
- [python docs guide](https://realpython.com/documenting-python-code/)
- check what is pydantic code

## TODO
- ValidationErrors and error handling in general
- *failsafe* function to catch generic success and raise
- move apis to `api/api_v1/endpoints/`
- use Depends() on proper places
- update schema and some more functionalities
- pytest? (TDD)
- user defined return types for all endpoints
- user OAuth headers properly, and attach the validation to all endpoints
