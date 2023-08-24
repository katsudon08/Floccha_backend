from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

import backend.analysis as analysis

# *ドキュメントは/docsに書かれている
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_headers = ["*"],
    allow_methods = ["*"]
)

class Request(BaseModel):
    src: list[str]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
async def write_root(req: Request):
    src = req.src
    print(src)
    data = analysis.execute(src)
    return data