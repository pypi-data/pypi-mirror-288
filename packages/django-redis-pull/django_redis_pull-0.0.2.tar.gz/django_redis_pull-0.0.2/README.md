### Installation
```bash
$ pip install django-redis-pull
```

#### `settings.py`
```python
INSTALLED_APPS+=['django_redis_pull']
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
+   data pull from redis to database
+   logging
    +   logging.debug messages
    +   database log
+   admin

### Models
model|db_table|fields/columns
-|-|-
`PullData`|`redis_push_data`|`id`,`queue`,`data`
`PushLog`|`redis_push_log`|`id`,`queue`,`count`,`created_at`
`PushQueue`|`redis_push_queue`|`id`,`queue`

### Management commands
name|description
-|-
`redis_pull`|pull redis data to `redis_pull_data (queue,data)` table

### Examples
```bash
$ python manage.py redis_pull
```

worker
```bash
$ python manage.py redis_pull_worker
```

