from opensearchpy import OpenSearch

def get_opensearch_client(host="localhost", port=9200) -> OpenSearch:
    # Create the client with SSL/TLS and hostname verification disabled.
    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_compress=True,
        use_ssl=False,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )
    return client

client = get_opensearch_client()

INDEX_NAME = "arxiv-cosine"

body = {
    "settings": {"index": {"knn": "true", "knn.algo_param.ef_search": 100}},
    "mappings": {
        "properties": {
            VECTOR_NAME: {
                "type": "knn_vector",
                "dimension": VECTOR_SIZE,
                "method": {
                    "name": "hnsw",
                    "space_type": "cosinesimil",
                    "engine": "nmslib",
                    "parameters": {"ef_construction": 128, "m": 24},
                },
            },
        }
    },
}
response = client.indices.create(INDEX_NAME, body=body)
