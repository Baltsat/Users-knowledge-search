import os
import json
from pipelines import process_collection


for fileName in filter((lambda f: 'pdf_processed' in f), os.listdir('./content')):
  with open(f'./content/{fileName}', 'r', encoding="utf8") as file:
    data = json.load(file)
    number = fileName.split('.')[0]
    for [k, v] in data.items():
      print(k, v)
    
    