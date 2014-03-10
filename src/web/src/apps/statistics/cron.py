import kronos
import elasticsearch

from .models import Snapshot


@kronos.register("*/5 * * * *")
def update_statistics():
    es = elasticsearch.Elasticsearch()

    print "Collecting stats..."
    stats = es.indices.stats("logs")["indices"]["logs"]["total"]
    snapshot = Snapshot()
    snapshot.total_count = stats["docs"]["count"]
    snapshot.store_size = stats["store"]["size_in_bytes"]
    snapshot.avg_fetch_time = stats["search"]["fetch_time_in_millis"]
    snapshot.total_queries = stats["search"]["query_total"]
    snapshot.save()