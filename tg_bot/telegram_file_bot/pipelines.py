import torch
from tqdm import tqdm
from pprint import pprint
from typing import Literal

from opensearch import client, INDEX_NAME, save_doc
from transformer import model, vectorized_doc


def process_doc(doc) -> None:
    try:
        doc = vectorized_doc(doc)
        save_doc(doc)
    except:
        print("Failed to process doc", doc)


def find(query):
    with torch.no_grad():
        mean_pooled = model.encode(query)

    query = {
        "size": 2,
        "query": {"knn": {"embedding": {"vector": mean_pooled, "k": 2}}},
        "_source": False,
        "fields": ["slide", "fileName", "description"],
    }

    response = client.search(body=query, index=INDEX_NAME)  # the same as before
    pprint(response["hits"]["hits"])
    return response["hits"]["hits"]
