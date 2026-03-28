psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    SELECT 'CREATE DATABASE post_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'post_db')\gexec
EOSQL