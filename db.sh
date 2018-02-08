#!/bin/bash
sudo apt-get update
sudo apt-get install python-pip python-dev python3-dev libpq-dev postgresql postgresql-contrib libz-dev libjpeg-dev libfreetype6-dev

echo "CREATE DATABASE punkweb; \
CREATE USER punkweb WITH PASSWORD 'punkweb'; \
ALTER ROLE punkweb SET client_encoding TO 'utf8'; \
ALTER ROLE punkweb SET timezone TO 'UTC'; \
GRANT ALL PRIVILEGES ON DATABASE punkweb TO punkweb;" | sudo su postgres -c psql

echo "create extension pg_trgm; " | sudo su postgres -c "psql -d punkweb"
