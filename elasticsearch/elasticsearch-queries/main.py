from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

doc = {
        "author": "csalaspe",
        "text": "Elasticsearch",
        "timestamp": datetime.now(),
        }

resp = es.index(index="test-hist-index1", id=1, document=doc)
print(resp["result"])
