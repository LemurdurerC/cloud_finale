import base64
import json
import string
import numpy as np
import uvicorn
from fastapi import FastAPI, File, UploadFile
import shutil
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch
from pytesseract import pytesseract, Output
import spacy
import os
import cv2
from magicPipeline import *
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()
#app.add_middleware(HTTPSRedirectMiddleware)
origins = [
    "https://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "https://localhost",
    "https://localhost:3000",
    "https://localhost:8000",
    "http://0.0.0.0",
    "https://0.0.0.0"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def create_upload_file(file: UploadFile = File(...)):
    print("test")
    test = file.file.read()
    test2 = np.frombuffer(test,np.uint8)
    try:
        img = cv2.imdecode(test2,cv2.IMREAD_COLOR)
        print("ok")
    except Exception as e:
        print("Lol")
    try:	
        data = magicPipeline(img)
    except Exception as e:
        print(e)
    sendElasticSearch(data)


def sendElasticSearch(datas):

    es = Elasticsearch(HOST="http://localhost", PORT=9200)
    es = Elasticsearch()
    print("je rentre dans la fonction elastic")
    ticket = {"id": "TESTID", "company": str(datas[0]),"date": str(datas[1]), "total": str(datas[2])}
    print(ticket)
    es.index(index="tickets", doc_type="text", body=ticket)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) #ssl_keyfile="/etc/apache2/server.key", ssl_certfile="/etc/apache2/server.crt")
