#!/bin/bash

pip install -r requirements.txt
psql postgres -c 'create database test_db;'

echo
echo "This will work"
pytest

echo
echo "*** This will not work ***"
flask db init
flask db migrate -m "Initial migration"
export DO_UPGRADE='true'
pytest

echo
echo "*** This won't work either ***"
pytest

echo
echo "*** This will work again ***"
export DO_UPGRADE=''
pytest
