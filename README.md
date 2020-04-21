# Pytest logging error

This repo intends to serve as a minimal working example of an obscure bug
where running `flask_migrate.upgrade()` inside of a test interferes
with logging for the rest of the test.

## Reproducing the issue

Assuming that you have `postgresql` running locally and `psql` installed, simply execute `run.sh`. Three tests are performed:

1. `pytest` with a blank database and no upgrade performed - this demonstrates that logging works initially.
2. `pytest` after initializing the database and creating a migration. The database is upgraded during the test. Logging works before the upgrade, but not after.
3. Same as the previous test, with the same result. The only difference is that there's no new migration to perform this time, demonstrating that it's just calling `flask_migrate.upgrade()` that causes the issue - not performing migration itself.
4. `pytest` without calling `flask_migrate.upgrade()` during the test. Logging works the whole time.

**NOTE**: To rerun `run.sh`, you should first execute `psql postgres -c 'drop database test_db;' && rm -rf migrations`

## Output

```
$ ./run.sh
Requirement already satisfied: flask in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from -r requirements.txt (line 1)) (1.1.2)
Requirement already satisfied: flask-migrate in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from -r requirements.txt (line 2)) (2.5.3)
Requirement already satisfied: flask-sqlalchemy in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from -r requirements.txt (line 3)) (2.4.1)
Requirement already satisfied: psycopg2 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from -r requirements.txt (line 4)) (2.8.5)
Requirement already satisfied: pytest in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from -r requirements.txt (line 5)) (5.4.1)
Requirement already satisfied: Jinja2>=2.10.1 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from flask->-r requirements.txt (line 1)) (2.11.2)
Requirement already satisfied: Werkzeug>=0.15 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from flask->-r requirements.txt (line 1)) (1.0.1)
Requirement already satisfied: click>=5.1 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from flask->-r requirements.txt (line 1)) (7.1.1)
Requirement already satisfied: itsdangerous>=0.24 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from flask->-r requirements.txt (line 1)) (1.1.0)
Requirement already satisfied: alembic>=0.7 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from flask-migrate->-r requirements.txt (line 2)) (1.4.2)
Requirement already satisfied: SQLAlchemy>=0.8.0 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from flask-sqlalchemy->-r requirements.txt (line 3)) (1.3.16)
Requirement already satisfied: more-itertools>=4.0.0 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from pytest->-r requirements.txt (line 5)) (8.2.0)
Requirement already satisfied: importlib-metadata>=0.12; python_version < "3.8" in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from pytest->-r requirements.txt (line 5)) (1.6.0)
Requirement already satisfied: pluggy<1.0,>=0.12 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from pytest->-r requirements.txt (line 5)) (0.13.1)
Requirement already satisfied: packaging in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from pytest->-r requirements.txt (line 5)) (20.3)
Requirement already satisfied: wcwidth in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from pytest->-r requirements.txt (line 5)) (0.1.9)
Requirement already satisfied: attrs>=17.4.0 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from pytest->-r requirements.txt (line 5)) (19.3.0)
Requirement already satisfied: py>=1.5.0 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from pytest->-r requirements.txt (line 5)) (1.8.1)
Requirement already satisfied: MarkupSafe>=0.23 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from Jinja2>=2.10.1->flask->-r requirements.txt (line 1)) (1.1.1)
Requirement already satisfied: python-dateutil in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from alembic>=0.7->flask-migrate->-r requirements.txt (line 2)) (2.8.1)
Requirement already satisfied: python-editor>=0.3 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from alembic>=0.7->flask-migrate->-r requirements.txt (line 2)) (1.0.4)
Requirement already satisfied: Mako in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from alembic>=0.7->flask-migrate->-r requirements.txt (line 2)) (1.1.2)
Requirement already satisfied: zipp>=0.5 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from importlib-metadata>=0.12; python_version < "3.8"->pytest->-r requirements.txt (line 5)) (3.1.0)
Requirement already satisfied: pyparsing>=2.0.2 in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from packaging->pytest->-r requirements.txt (line 5)) (2.4.7)
Requirement already satisfied: six in /home/oliver/local/miniconda3/envs/pytest-bug/lib/python3.7/site-packages (from packaging->pytest->-r requirements.txt (line 5)) (1.14.0)
CREATE DATABASE

*** This will work ***
======================================= test session starts =======================================
platform linux -- Python 3.7.7, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
rootdir: /home/oliver/code/python/pytest-logging-bug
collected 1 item                                                                                  

app_test.py .                                                                               [100%]

======================================== 1 passed in 0.21s ========================================

*** This will not work ***
  Creating directory /home/oliver/code/python/pytest-logging-bug/migrations ...  done
  Creating directory /home/oliver/code/python/pytest-logging-bug/migrations/versions ...  done
  Generating /home/oliver/code/python/pytest-logging-bug/migrations/README ...  done
  Generating /home/oliver/code/python/pytest-logging-bug/migrations/alembic.ini ...  done
  Generating /home/oliver/code/python/pytest-logging-bug/migrations/env.py ...  done
  Generating /home/oliver/code/python/pytest-logging-bug/migrations/script.py.mako ...  done
  Please edit configuration/connection/logging settings in '/home/oliver/code/python/pytest-logging-
  bug/migrations/alembic.ini' before proceeding.
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'tasks'
  Generating /home/oliver/code/python/pytest-logging-
  bug/migrations/versions/20a337f6c148_initial_migration.py ...  done
======================================= test session starts =======================================
platform linux -- Python 3.7.7, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
rootdir: /home/oliver/code/python/pytest-logging-bug
collected 1 item                                                                                  

app_test.py F                                                                               [100%]

============================================ FAILURES =============================================
__________________________________________ test_logging ___________________________________________

app_fixture = None, caplog = <_pytest.logging.LogCaptureFixture object at 0x7f6eeaf74050>

    def test_logging(app_fixture, caplog):
        msg1 = "Before"
        logging.info(msg1)
    
        if os.getenv('DO_UPGRADE'):
            flask_migrate.upgrade()
    
        msg2 = "After"
        logging.info(msg2)
>       assert [msg1, msg2] == [rec.message for rec in caplog.records]
E       AssertionError: assert ['Before', 'After'] == ['Before']
E         Left contains one more item: 'After'
E         Use -v to get the full diff

app_test.py:32: AssertionError
-------------------------------------- Captured stderr call ---------------------------------------
INFO:root:Before
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 20a337f6c148, Initial migration
---------------------------------------- Captured log call ----------------------------------------
INFO     root:app_test.py:25 Before
===================================== short test summary info =====================================
FAILED app_test.py::test_logging - AssertionError: assert ['Before', 'After'] == ['Before']
======================================== 1 failed in 0.28s ========================================

*** This won't work either ***
======================================= test session starts =======================================
platform linux -- Python 3.7.7, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
rootdir: /home/oliver/code/python/pytest-logging-bug
collected 1 item                                                                                  

app_test.py F                                                                               [100%]

============================================ FAILURES =============================================
__________________________________________ test_logging ___________________________________________

app_fixture = None, caplog = <_pytest.logging.LogCaptureFixture object at 0x7fb467acf090>

    def test_logging(app_fixture, caplog):
        msg1 = "Before"
        logging.info(msg1)
    
        if os.getenv('DO_UPGRADE'):
            flask_migrate.upgrade()
    
        msg2 = "After"
        logging.info(msg2)
>       assert [msg1, msg2] == [rec.message for rec in caplog.records]
E       AssertionError: assert ['Before', 'After'] == ['Before']
E         Left contains one more item: 'After'
E         Use -v to get the full diff

app_test.py:32: AssertionError
-------------------------------------- Captured stderr call ---------------------------------------
INFO:root:Before
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
---------------------------------------- Captured log call ----------------------------------------
INFO     root:app_test.py:25 Before
===================================== short test summary info =====================================
FAILED app_test.py::test_logging - AssertionError: assert ['Before', 'After'] == ['Before']
======================================== 1 failed in 0.27s ========================================

*** This will work again ***
======================================= test session starts =======================================
platform linux -- Python 3.7.7, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
rootdir: /home/oliver/code/python/pytest-logging-bug
collected 1 item                                                                                  

app_test.py .                                                                               [100%]

======================================== 1 passed in 0.21s ========================================
```

# Update

Based on @miguelgrinberg's advice in [Flask-Migrate#330](https://github.com/miguelgrinberg/Flask-Migrate/issues/330), the simplest solution is to run `flask_migrate.upgrade()` as a subprocess: [Solution diff](https://github.com/OliverEvans96/pytest-logging-bug/pull/1/files)
