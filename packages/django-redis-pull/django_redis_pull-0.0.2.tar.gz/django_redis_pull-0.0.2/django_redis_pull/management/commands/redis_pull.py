import collections
import json
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from ...redis_client import REDIS_CLIENT
from ...models import PullData, PullLog, PullQueue

PREFETCH_COUNT = 10000

class Command(BaseCommand):
    def handle(self, *args, **options):
        bulk_create_list = []
        queue_list = list(PullQueue.objects.values_list('name',flat=True))
        if not queue_list:
            raise NotImplementedError('unknown pull queue')
        queue2count = collections.defaultdict(int)
        for queue in queue_list:
            pipe = REDIS_CLIENT.pipeline()
            pipe.lrange(queue, 0, PREFETCH_COUNT - 1)
            pipe.ltrim(queue, PREFETCH_COUNT, -1)
            data_list, trim_success = pipe.execute()
            for data in data_list:
                bulk_create_list += [PullData(queue=queue, data=json.loads(data))]
                queue2count[queue]+=1
        for queue,count in queue2count.items():
            logging.debug('REDIS PULL: %s (%s)' % (queue,count))
            bulk_create_list += [PullLog(queue=queue, count=count)]
        for model in set(map(lambda i:type(i),bulk_create_list)):
            _bulk_create_list = list(filter(lambda i:type(i)==model,bulk_create_list))
            model.objects.bulk_create(_bulk_create_list)
