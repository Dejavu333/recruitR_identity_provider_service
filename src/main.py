import datetime
import json
import os

import jwt
from fastapi import FastAPI, HTTPException, Request
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr, constr
from starlette.middleware.cors import CORSMiddleware

####################################################
# setup 
####################################################
app = FastAPI()  # webapp
# allow same origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PRIVATE_KEY = os.getenv("PRIVATE_KEY_ENVV", "supersecret")  # key to sign the JWT
HOST = os.getenv("HOST_ENVV", "localhost")
PORT = int(os.getenv("PORT_ENVV", "6000"))
users = {"test@test.com": "testtest", "test2@test2.com": "test2test2"}

security = HTTPBearer()

# validation
# todo central syntactic validaiton, and domain specific validation in the downstream services, maybe schema repo
class User(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

class Token(BaseModel):
    token: str

####################################################
# functions
####################################################
def save_openapi_spec_to_file():
    with open("../docs/OAS.json", "w") as f:
        json.dump(app.openapi(), f , indent=2)

# openApi spec
def setup_host_in_openapi_spec():
    openapi_schema = app.openapi()
    openapi_schema["servers"] = [{
            "url": f"http://localhost:{PORT}" # if docker debug and windows OS, use http://host.docker.internal to reach host machine
        }]

def setupOpenApi():
    setup_host_in_openapi_spec()
    save_openapi_spec_to_file()

####################################################
# routes
####################################################
# register
@app.post('/api/v1/register')
def register(user: User):
    if user.email in users:
        raise HTTPException(status_code=400, detail="User already exists!")
    users[user.email] = user.password
    return {"message": "User registered successfully!"}

# login
@app.post('/api/v1/authN', response_model=Token)
def authenticate(user: User):
    if users.get(user.email) == user.password:
        token = jwt.encode({
            'user': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, PRIVATE_KEY)
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials!")

# authorize
@app.get('/api/v1/authZ')
async def authorize(request: Request):
    auth = await security(request)
    token = auth.credentials
    try:
        decoded = jwt.decode(token, PRIVATE_KEY, algorithms=["HS256"])
        return {"user": decoded["user"], "message": "Authorized"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired!")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token!")

####################################################
# main
####################################################
if __name__ == '__main__':
    setupOpenApi()
    import uvicorn # asynchronous server implementation
    uvicorn.run(app, host=HOST, port=PORT)