```
docker run --name es-node01 --net elastic -p 9200:9200 -p 9300:9300 -t docker.elastic.co/elasticsearch/elasticsearch:
```

If errors max virtual memory:
```
sysctl -w vm.max_map_count=262144
```

Create index with two field mappings:
- `my_histogram`, a `histogram` field used to store percentile data
- `my_text`, a `keyword` field used to store a title for the histogram

```
curl -X PUT "localhost:9200/my-index-000001?pretty" -H 'Content-Type: application/json' -d'
{
  "mappings" : {
    "properties" : {
      "my_histogram" : {
        "type" : "histogram"
      },
      "my_text" : {
        "type" : "keyword"
      }
    }
  }
}
'
```

Store pre-aggregated for two histograms: `histogram_1` and `histogram_2`:

```
curl -X PUT "localhost:9200/my-index-000001/_doc/1?pretty" -H 'Content-Type: application/json' -d'
{
  "my_text" : "histogram_1",
  "my_histogram" : {
      "values" : [0.1, 0.2, 0.3, 0.4, 0.5], 
      "counts" : [3, 7, 23, 12, 6] 
   }
}
'
curl -X PUT "localhost:9200/my-index-000001/_doc/2?pretty" -H 'Content-Type: application/json' -d'
{
  "my_text" : "histogram_2",
  "my_histogram" : {
      "values" : [0.1, 0.25, 0.35, 0.4, 0.45, 0.5], 
      "counts" : [8, 17, 8, 7, 6, 2] 
   }
}
'
```

Correlate latency - K-S test correlation aggregation:

```
curl -X POST "localhost:9200/correlate_latency/_search?size=0&filter_path=aggregations&pretty" -H 'Content-Type: application/json' -d'
{
  "aggs": {
    "buckets": {
      "terms": { 
        "field": "version",
        "size": 2
      },
      "aggs": {
        "latency_ranges": {
          "range": { 
            "field": "latency",
            "ranges": [
              { "to": 0 },
              { "from": 0, "to": 105 },
              { "from": 105, "to": 225 },
              { "from": 225, "to": 445 },
              { "from": 445, "to": 665 },
              { "from": 665, "to": 885 },
              { "from": 885, "to": 1115 },
              { "from": 1115, "to": 1335 },
              { "from": 1335, "to": 1555 },
              { "from": 1555, "to": 1775 },
              { "from": 1775 }
            ]
          }
        },
        "ks_test": { 
          "bucket_count_ks_test": {
            "buckets_path": "latency_ranges>_count",
            "alternative": ["less", "greater", "two_sided"]
          }
        }
      }
    }
  }
}
'
```

{
  "bucket_count_ks_test": {
    "buckets_path": "range_values>_count", 
    "alternative": ["less", "greater", "two_sided"], 
    "fractions": "counts"
  }
}

curl -X POST "localhost:9200/correlate_latency/_search?size=0&filter_path=aggregations&pretty" -H 'Content-Type: application/json' -d'
{
  "aggs": {
    "buckets": {
      "terms": { 
        "field": "version",
        "size": 2
      },
      "aggs": {
        "ks_test": { 
          "bucket_count_ks_test": {
            "buckets_path": "my_histogram_1>counts", 
            "alternative": ["two_sided"], 
            "sampling_method": "upper_tail",
            "fractions":"my_histogram_2>counts"
          }
        }
      }
    }
  }
}
'

{
  "bucket_count_ks_test": {
    "buckets_path": "my_histogram_1>counts", 
    "alternative": "two_sided"], 
    "sampling_method": "upper_tail",
    "fractions":"my_histogram_2>counts"
  }
}
