### Installation
```bash
$ pip install django-redis-push
```

#### `settings.py`
```python
INSTALLED_APPS+=['django_redis_push']
```

#### `migrate`
```bash
$ python manage.py migrate
```

### Environment variables
Variable|default
-|-
`REDIS_HOST`|`localhost`
`REDIS_PORT`|`6379`
`REDIS_DB`|`0`

### Features
+   data push from database to redis
+   logging
    +   logging.debug messages
    +   database log

### Models
model|db_table|fields/columns
-|-|-
`PushData`|`redis_push_data`|`id`,`queue`,`data`
`PushLog`|`redis_push_log`|`id`,`queue`,`count`,`created_at`

### Management commands
name|description
-|-
`redis_push`|push `PushData`/`redis_push_data` to redis

### Examples
```bash
$ python manage.py redis_push
```

```python
from django.core.management import call_command

call_command("redis_push")
```

