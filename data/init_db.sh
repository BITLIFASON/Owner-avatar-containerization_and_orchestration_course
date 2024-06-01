#!/bin/bash

sleep 10

# Ждем, пока база данных станет доступной
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE $POSTGRES_DB_APP;
    CREATE USER $POSTGRES_USER_APP WITH ENCRYPTED PASSWORD '$POSTGRES_PASSWORD_APP';
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB_APP TO $POSTGRES_USER_APP;
EOSQL

echo "database was created successfully"