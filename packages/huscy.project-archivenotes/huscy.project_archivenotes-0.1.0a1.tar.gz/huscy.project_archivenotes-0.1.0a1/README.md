huscy.project_archivenotes
======

![alt](https://img.shields.io/pypi/v/huscy-project-archivenotes.svg)
![alt](https://img.shields.io/pypi/pyversions/huscy-project-archivenotes.svg)



Requirements
------

- Python 3.6+
- A supported version of Django

Tox tests on Django versions 2.2, 3.2 and 4.0.



Installation
------

To install `husy.project_archivenotes` simply run:
```
pip install huscy.project_archivenotes
```


Configuration
------

We need to hook `huscy.project_archivenotes` into our project.

1. Add `huscy.project_archivenotes` into your `INSTALLED_APPS` at settings module:

```python
INSTALLED_APPS = (
	...
	'huscy.project_archivenotes',
	'huscy.projects',
)
```

2. Create `huscy.project_archivenotes` database tables by running:

```
python manage.py migrate
```


Development
------

After checking out the repository you should run

```
make install
```

to install all development and test requirements and

```
make migrate
```

to create the database tables.
We assume you have a running postgres database with a user `huscy` and a database also called `huscy`.
You can easily create them by running

```
sudo -u postgres createuser -d huscy
sudo -u postgres psql -c "ALTER USER huscy WITH PASSWORD '123'"
sudo -u postgres createdb huscy
```
