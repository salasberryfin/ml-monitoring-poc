import json
from datetime import datetime

from calc_drift import get_drift

from elasticsearch import Elasticsearch

DRIFT_RESULT_FILE = "bike-data-drift-result-3.json"
es = Elasticsearch("http://localhost:9200")


def create_index():
    """
    Create a new Elasticsearch index
    The creation of an index is implicit when sending data to an index that
    is not recognized
    """
    # create index
    doc = {
        "title":    {"type": "text"},
        "name":     {"type": "text"},
        "pvalue":   {"type": "integer"},
        "datetime": {"type": "text"},
        "created":  {
            "type":   "date",
            "format": "strict_date_optional_time||epoch_millis"
        }
    }

    new_index = es.index(index="index-test-data-drift", id=1, document=doc)
    print(new_index["result"])


def publish_to_index():
    """
    Send data to Elasticsearch
    """
    data = []
    with open(DRIFT_RESULT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    # features: data["data_drift"]["data"]["num_feature_names"]
    # p_value: data["data_drift"]["data"]["metrics"][<feature>]["p_value"]
    drift_datetime = datetime.strptime(
        data["data_drift"]["datetime"],
        "%Y-%m-%d %H:%M:%S.%f",
    )
    data = data["data_drift"]["data"]
    metrics = data["metrics"]
    p_values = {
        feat: metrics[feat]["p_value"] for feat in data["num_feature_names"]
    }

    current = datetime.now()
    for key, value in p_values.items():
        doc = {
            "title": "automatic-drift-logging",
            "name": key,
            "drift": {
                "pvalue": value,
                "drift": get_drift(value),
            },
            # `datetime` - timestamp of drift results
            "datetime": drift_datetime,
            # `index_created` - when is the index published to EKS
            "index_created": current,
        }

        global_index_name = "bike-data-drift"
        print(f"Sending data to global index {global_index_name}")
        resp = es.index(
            index=global_index_name,
            document=doc
        )

        print(resp["result"])

        # index_name = key.replace(" ", "-")
        # print(f"Sending data to feature specific index {index_name}")
        # resp = es.index(
        #     index=index_name,
        #     document=doc
        # )

        # print(resp["result"])


if __name__ == "__main__":
    publish_to_index()
