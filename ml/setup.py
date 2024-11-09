from opensearch import client, INDEX_NAME

settings = {
    "settings": {
        "index": {
            "knn": True,
        }
    },
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "id": {"type": "integer"},
            "description": {"type": "text"},
            "embedding": {
                "type": "knn_vector",
                "dimension": 1024,
            },
        }
    },
}

res = client.indices.create(index=INDEX_NAME, body=settings, ignore=[400])
print(f'✅ Inited index: {INDEX_NAME}')

