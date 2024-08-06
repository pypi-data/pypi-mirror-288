=====
AutoJob
=====

AutoJob is a simple Django app to conduct Web-based autojob. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------
#### 1. Add "autojob" to your INSTALLED_APPS setting like this
```
    INSTALLED_APPS = [
        ...
        'autojob.apps.AutoJob',
    ]
```
#### 2. Run `python manage.py migrate` to create the autojob models


#### 3. Add a reference to `wsgi.py`::
```
    from autojob import job_tool
    job_tool.job_control()
```
#### 4. Add cache config to settings.py
```
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/0",
            "OPTIONS": {
                "PICK_VERSION": -1,
                "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PASSWORD": ""
            }
        }
    }
```
#### 5. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

#### 6. Visit http://127.0.0.1:8000/admin/autojob/ to participate in the poll.