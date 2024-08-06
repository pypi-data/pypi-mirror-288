from django.conf import settings
from elasticsearch import Elasticsearch

from core.celery import APP


@APP.task()
def send_logs_to_elk(data):
    try:
        elastic_search = Elasticsearch(hosts=settings.ELK_LOGGER_URL)
        result = elastic_search.index(index=settings.APP_NAME.lower(), body=data)
        return result
    except Exception as e:
        print(f"Failed to index data into Elasticsearch: {e}")
