#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

# Function to check if postgres is ready
check_postgres() {
    PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -d "postgres" -c "SELECT 1" > /dev/null 2>&1
}

# Function to check if our database exists
check_database() {
    PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -d "postgres" -c "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'" | grep -q 1
}

# Function to create database if it doesn't exist
create_database() {
    PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -d "postgres" -c "CREATE DATABASE $POSTGRES_DB"
}

echo "Waiting for postgres..."
until check_postgres; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

echo "Postgres is up - checking for database..."
if ! check_database; then
    echo "Database $POSTGRES_DB does not exist. Creating..."
    create_database
    echo "Database created."
fi

>&2 echo "Postgres is up and database exists - executing command"
exec $cmd 