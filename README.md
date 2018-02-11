## STR:

1. Clone this repo
2. `pip install https://github.com/django/django/archive/master.zip`
3. `./manage.py migrate`
4. `cp testapp/models_new.py testapp/models.py`
5. `./manage.py makemigrations --name broken_migration`
6. `./manage.py migrate`

## Expected:

New migration is created/applied successfully.

## Actual:

The new `0002_broken_migration.py` migration incorrectly lists the `RemoveField`
operation before the `AlterUniqueTogether` operation...

```py
    operations = [
        migrations.RemoveField(
            model_name='push',
            name='foo',
        ),
        migrations.AlterUniqueTogether(
            name='push',
            unique_together={('repository', 'revision')},
        ),
    ]
```

Which results in an exception at step 6...

```
$ ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, testapp
Running migrations:
  Applying testapp.0002_broken_migration...Traceback (most recent call last):
  File ".../site-packages/django/db/models/options.py", line 564, in get_field
    return self.fields_map[field_name]
KeyError: 'foo'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  ...
  File ".../site-packages/django/db/backends/base/schema.py", line 286, in create_model
    columns = [model._meta.get_field(field).column for field in fields]
  File ".../site-packages/django/db/backends/base/schema.py", line 286, in <listcomp>
    columns = [model._meta.get_field(field).column for field in fields]
  File ".../site-packages/django/db/models/options.py", line 566, in get_field
    raise FieldDoesNotExist("%s has no field named '%s'" % (self.object_name, field_name))
django.core.exceptions.FieldDoesNotExist: Push has no field named 'foo'
```

## Additional notes:
* This affects both the SQLite backend and the MySQL backend (others not tested).
* If the `('repository', 'revision')` entry in `unique_together` is omitted from
  both the original and new models, then the bug does not occur.
* At time of testing, django master was at revision `6d794fb76212bb8a62fe2cd97cff173054e1c626`.
* This also affects Django 1.11.10.
* The above was using Python 3.6.2. 
