# Single-store docker file
# https://github.com/z0rr0/single-store/
# Version z0rr0/single-store:0.1.4
# It is an Alpine based containter for python3 django applications.

FROM alpine:edge
MAINTAINER Alexander Zaytsev "thebestzorro@yandex.ru"

RUN apk update && apk upgrade
RUN apk add tzdata ca-certificates python3 python3-dev uwsgi-python3 gcc build-base jpeg-dev zlib-dev mariadb-client-libs mariadb-dev git

RUN pip3 install docutils pillow ipython mysqlclient django-debug-toolbar Django==1.11

# build and install django-geoip exclude standard pip due temporary migration bug
RUN cd /tmp && \
    git clone https://github.com/futurecolors/django-geoip.git && \
    cd django-geoip && \
    python3 setup.py sdist && \
    pip3 install dist/django-geoip-*.tar.gz && \
    cd / && rm -rf /tmp/django-geoip

VOLUME ["/data/conf", "/var/store/store/media/product_images"]
ADD store /var/store

RUN rm -f /var/store/store/settings_local.py /var/store/store/settings.py && \
    ln -s /data/conf/settings_local.py /var/store/store/settings_local.py && \
    ln -s /data/conf/settings.py /var/store/store/settings.py

EXPOSE 23432
WORKDIR /var/store
ENTRYPOINT ["/usr/sbin/uwsgi"]
CMD ["--ini", "/data/conf/uwsgi_store.ini"]

# docker compose example
# store:
#   restart: always
#   image: "z0rr0/single-store:latest"
#   ports:
#     - "23432:23432"
#   volumes:
#     - "/data/store/conf:/data/conf:ro"
#     - "/data/store/product_images:/var/store/store/media/product_images"
#   links:
#     - "mariadb:mariadb"
#   log_driver: "json-file"
#   log_opt:
#     max-size: "16m"
#     max-file: "5"
