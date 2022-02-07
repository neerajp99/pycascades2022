from typing import Optional

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import the json object from the db.json
import json
db = json.load(open('db.json'))

@app.get("/", status_code=200)
def show_talks():
    return db

# Create a method that takes in talk id and returns the talk object from the db.json
@app.get("/talk/{id}")
def get_talk(id: str):
    try:
        for talk in db:
            if talk['talk_id'] == id:
                return JSONResponse (
                    status_code = 200, 
                    content = {"talk": talk}
                )
        return JSONResponse(status_code=404, content={"Talk not found"})
    except:
        raise HTTPException(status_code=404, detail="Talk not found")
        return {"error": "Talk not found"}

    