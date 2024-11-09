from opensearchpy import OpenSearch, helpers

INDEX_NAME = "recipe"

client = OpenSearch(
    hosts=["http://admin:jW6%3FX4P8g3%2C@localhost:9200/"],
    http_compress=True,
    use_ssl=False,  # DONT USE IN PRODUCTION
    verify_certs=False,  # DONT USE IN PRODUCTION
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

# Create indicies


def save_doc(slides):
  helpers.bulk(client, slides, index=INDEX_NAME, raise_on_error=True, refresh=True)

