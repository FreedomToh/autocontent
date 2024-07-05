FROM postgres:14

# Установите пакет gettext, который включает в себя envsubst
RUN apt-get update && apt-get install -y gettext && rm -rf /var/lib/apt/lists/*

# Скопируйте ваш скрипт в образ
COPY ./init/init.sql /docker-entrypoint-initdb.d/init.sql

# Сделайте скрипт исполняемым
RUN chmod +x /docker-entrypoint-initdb.d/init.sql

# Используйте стандартный entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]

# Передайте аргументы командной строки в entrypoint
CMD ["postgres"]