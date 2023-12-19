
# Student Management

## Overview of commands
```bash
cd "C:\Users\user\Documents\tasks\student-mgmt\"
cd app
..\venv\Scripts\activate
uvicorn main:router --reload
```
## Just in case
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
service.namespace
## Kubectl commands
```bash
docker context ls
docker use default

minikube start --addons=ingress

minikube addons enable ingress

minikube docker-env

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.0/deploy/static/provider/cloud/deploy.yaml

kubectl apply -f .\backend\k8-backend.yaml
deployment.apps/mini-school-be-deployment unchanged
service/mini-school-be-service unchanged

kubectl apply -f .\database\k8-database.yaml
deployment.apps/mini-school-db-deployment configured
service/mini-school-db-service unchanged

kubectl create configmap db-configmap --from-env-file .\.env

kubectl describe configmaps postgres-configmap

kubectl get deployments

kubectl get services

minikube service mini-school-db-service

minikube service mini-school-be-service

port-forward service/mini-school-be-service 80:80
kubectl exec -it mini-school-be-deployment-58bc45cf8d-245m7 bash
 
```
# Diagnostics

```bash
docker login 
docker context ls
docker context use default
kubectl config use-context minikube
kubectl get events
kubectl get pods
minikube image load postgres:0.0.1
minikube image load mini-school:0.0.1
kubectl describe configmaps postgres-configmap
kubectl logs -f mini-school-db-deployment-6cf854ccd4-62wgz
kubectl edit deploy mini-school-db-deployment
kubectl describe pod mini-school-db-deployment-6cf854ccd4-8ppbd
```

# Ongoing Refactor tasks
1. Move orm files inside database & common to model & schema 
2. Restructuring class

## TODO
- ValidationErrors
- cascade delete records
- *failsafe* function to catch generic success and raise
- move apis to routers/
- schema design
- look for auto documentations
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
