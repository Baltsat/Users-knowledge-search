import aiofiles
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from process_pdf import process_and_save
from pipelines import find
from seed_by_file import seed_by_file

DOWNLOAD_PATH = '/app/downloads'

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

@app.post('/upload')
async def search_endpoint(
    document: UploadFile = File(description="Your document (max 10 MB)"),
):
  file_path = f"{DOWNLOAD_PATH}/{document.filename}"
  async with aiofiles.open(file_path, 'wb') as out_file:
      content = await document.read()  # async read
      await out_file.write(content)  # async write
  json_output = process_and_save(file_path)
  return seed_by_file(f'{document.filename}_processed.json', DOWNLOAD_PATH)

if __name__ == "__main__":
  uvicorn.run("app:app", reload=True, use_colors=True, host="0.0.0.0", port=8000)