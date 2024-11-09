import cohere
import json

import numpy as np 
from typing import List, Union 

texts = [
    ''
]

def get_cohere_embedding(
    text: Union[str, List[str]], model_name: str = "embed-english-light-v2.0"
) -> List[float]:
    """
    Embed a single text with cohere client and return list of floats
    """
    if type(text) == str:
        embed = co.embed([text], model=model_name).embeddings[0]
    else:
        embed = co.embed(text, model=model_name).embeddings
    return embed


embed_list = get_cohere_embedding(texts)
cache = dict(zip(texts, embed_list))

with open("cache.jsonl", "w") as fp:
    json.dump(cache, fp)
  


def find_similar_docs(query: str, k: int, num_results: int, index_name: str) -> Dict:
    """
    Main semantic search capability using knn on input query strings.
    Args:
        k: number of top-k similar vectors to retrieve from OpenSearch index
        num_results: number of the top-k similar vectors to retrieve
        index_name: index name in OpenSearch
    """
    embed_vector = get_cohere_embedding(query)

    body = {
        "size": num_results,
        "query": {"knn": {VECTOR_NAME: {"vector": embed_vector, "k": k}}},
    }

    url = f"<http://localhost:9200/{index_name}/_search>"
    response = requests.get(
        url, json=body, headers={"Content-Type": "application/json"}
    )
    return json.loads(response.content)
