# -*- coding: utf-8 -*-
import os
from model_utils import load_model, make_inference
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests


class Instance(BaseModel):
    cylinders: int
    displacement: float
    horsepower: float
    weight: float
    acceleration: float
    model_year: int
    origin: int


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_url = "http://auth_server:8500"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=auth_url + "/token")
model_path = "models/pipeline.pkl"
if model_path is None:
    raise ValueError("The environment variable $MODEL_PATH is empty!")


async def check_token(token: str = Depends(oauth2_scheme)):
    post_response = requests.post(auth_url + "/get_user?token=" + token)
    if post_response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return post_response.json()


@app.get("/healthcheck")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/users/me")
async def read_users_me(current_user: str = Depends(check_token)):
    return current_user


@app.post("/predictions")
async def predictions(instance: Instance,
                      token: str = Depends(check_token)) -> dict[str, float]:
    return make_inference(load_model(model_path), instance.dict())
