# Single-store docker file
# https://github.com/z0rr0/single-store/
# Version 1.0
# It is an Alpine based containter for python3 django applications.

FROM alpine:edge
MAINTAINER Alexander Zaytsev "thebestzorro@yandex.ru"

RUN apk update && apk upgrade && mkdir /var/wwww
RUN apk add tzdata ca-certificates python3 python3-dev uwsgi-python3 && gcc build-base jpeg-dev zlib-dev git

RUN pip3 install docutils pillow ipython Django==1.11

# build and install django-geoip exclude stadart pip
RUN cd /tmp && \
    git clone https://github.com/futurecolors/django-geoip.git && \
    cd django-geoip && \
    python3 setup.py sdist && \
    pip3 install dist/django-geoip-*.tar.gz && \
    cd / && \
    rm -rf /tmp/django-geoip

# VOLUME ["/data/conf/"]
# ADD store /var/wwww/

RUN rm -f /var/www/store/store/local_settings.py /var/www/store/store/settings.py && \
    ln -s /data/conf/single-store/settings_local.py /var/www/store/store/local_settings.py && \
    ln -s /data/conf/single-store/settings.py /var/www/store/store/settings.py

# EXPOSE 23432
# WORKDIR /var/www
# ENTRYPOINT ["/usr/bin/uwsgi"]
# CMD ["--ini", "/data/conf/single-store/conf.ini"]
