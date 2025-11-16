# postgres.Dockerfile
FROM postgres:15

# Optional: copy initial SQL schema
# COPY init.sql /docker-entrypoint-initdb.d/

# Environment variables are set in docker-compose.yml
