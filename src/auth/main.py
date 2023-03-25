
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "3c19620880afb6abbca093abe56e3820a45c0dc8c796e58420d6a34f4e2fba31"
ALGORITHM = "HS256"

# this function will create the token
# for particular data
def create_access_token(data: dict):
    to_encode = data.copy()
     
    # expire time of the token
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
     
    # return the generated token
    return encoded_jwt

# the endpoint to verify the token
@app.post("/get_user")
async def get_user(token: str):
    try:
        # try to decode the token, it will
        # raise error if the token is not correct
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

@app.post("/token")
def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # data to be signed using token
    data = {
        'user': form_data.username
    }
    token = create_access_token(data=data)
    return { "access_token" : token }