import collections
import json
import logging
import time

from django.core.management.base import BaseCommand

from ...redis_client import REDIS_CLIENT
from ...models import PushData, PushLog


class Command(BaseCommand):
    def handle(self, *args, **options):
        data_list = []
        queue2count = collections.defaultdict(int)
        push_list = list(PushData.objects.order_by('id')[0:10000])
        for push in push_list:
            queue2count[push.queue]+=1
            data_list+=[json.dumps(push.data)]
        if push_list:
            REDIS_CLIENT.rpush(push.queue, *data_list)
            PushData.objects.filter(
                id__lte=max(map(lambda p: p.id, push_list))
            ).delete()
        bulk_create_list = []
        for queue,count in queue2count.items():
            logging.debug('REDIS PUSH: %s (%s)' % (queue,count))
            bulk_create_list += [PushLog(queue=queue,count=count)]
        PushLog.objects.bulk_create(bulk_create_list)
