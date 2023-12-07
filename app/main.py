from fastapi import FastAPI

router = FastAPI()

@router.get("/", response_model=dict, status_code=200)
def get_status():

    '''
    Get the status of the server
    '''

    return {"status" : "Server up and running!"}

