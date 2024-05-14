FROM postgres:latest

ENV POSTGRES_USER=egemen
ENV POSTGRES_PASSWORD=egemen123

EXPOSE 5432

ENV POSTGRES_DB=EMERGENCY_ROBOT_DB
ENV POSTGRES_INITDB_ARGS="--encoding=UTF-8 --lc-collate=C --lc-ctype=C --data-checksums"

CMD [ "postgres" ]