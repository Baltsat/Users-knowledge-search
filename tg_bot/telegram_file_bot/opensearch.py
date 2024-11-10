from opensearchpy import OpenSearch, helpers
from config import OPENSEARCH_HOST

INDEX_NAME = "recipe"

client = OpenSearch(
    hosts=[OPENSEARCH_HOST],
    http_compress=True,
    use_ssl=False,  # DONT USE IN PRODUCTION
    verify_certs=False,  # DONT USE IN PRODUCTION
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

# Create indicies


def save_doc(slides):
  helpers.bulk(client, slides, index=INDEX_NAME, raise_on_error=True, refresh=True)

