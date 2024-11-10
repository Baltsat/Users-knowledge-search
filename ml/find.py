from typing import Literal
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch
import torch
from pprint import pprint


INDEX_NAME = "recipe"
device: Literal['cuda:0'] | Literal['cpu'] = "cuda:0" if torch.cuda.is_available() else "cpu"

model = SentenceTransformer("BAAI/bge-m3")

client = OpenSearch(
    hosts=["http://admin:jW6%3FX4P8g3%2C@localhost:9200/"],
    http_compress=True,
    use_ssl=False,  # DONT USE IN PRODUCTION
    verify_certs=False,  # DONT USE IN PRODUCTION
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

text = "персональных данные"

with torch.no_grad():
    mean_pooled = model.encode(text)

query = {
    "size": 10,
    "query": {"knn": {"embedding": {"vector": mean_pooled, "k": 3}}},
    "_source": False,
    "fields": ["id", "name", "description"],
}

response = client.search(body=query, index=INDEX_NAME)  # the same as before
pprint(response["hits"]["hits"])
