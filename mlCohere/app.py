import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kotaemon.base import Document, DocumentWithEmbedding

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, use_colors=True)
  
