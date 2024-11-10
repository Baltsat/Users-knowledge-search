import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipelines import find


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Search(BaseModel):
  query: str

@app.post('/search')
def search_endpoint(req: Search):
  return find(req.query)


if __name__ == "__main__":
  uvicorn.run("app:app", reload=True, use_colors=True)