# single-store
Single Store


## Test

```bash
cd store
python manage.py test --pythonpath $PWD -v 2
```

## Localization

```bash
python manage.py makemessages --locale=ru_RU
# edit *.po files
python manage.py compilemessages --locale=ru_RU
```