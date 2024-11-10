import torch
from typing import Literal
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('BAAI/bge-m3')
device: Literal['cuda:0'] | Literal['cpu'] = "cuda:0" if torch.cuda.is_available() else "cpu"

def vectorized_doc(slides):
  with torch.no_grad():
    mean_pooled = model.encode([slide["description"] for slide in slides])
  for slide, vec in zip(slides, mean_pooled):
    slide["embedding"] = vec
  
  del mean_pooled 
  torch.cuda.empty_cache()

  return slides
