import elasticsearch
es = elasticsearch.Elasticsearch()

if not es.indices.exists("test"):
    es.indices.create("test")

for i in xrange(7):
    es.index("test", ".percolator", {"query":{"query_string":{"query":"a OR b"}}}, id=str(i))

for i in xrange(7):
    es.delete("test", ".percolator", str(i))

x = es.index("test", "test", {"a":"b"})
print es.percolate("test", "test", x["_id"])