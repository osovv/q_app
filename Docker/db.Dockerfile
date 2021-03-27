FROM postgres:13.2
COPY 01-init.sh /docker-entrypoint-initdb.d/