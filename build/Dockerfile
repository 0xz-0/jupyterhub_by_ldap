FROM jupyterhub/jupyterhub:2.1.1
# url: https://hub.docker.com/r/jupyterhub/jupyterhub

USER root

RUN sed -i "s/httpredir.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN sed -i "s/security.debian.org/mirrors.aliyun.com\/debian-security/g" /etc/apt/sources.list

RUN apt-get clean

RUN apt-get update &&\
    apt-get -y install vim &&\
    apt-get -y install build-essential &&\
    apt-get -y install python3-dev &&\
    apt-get -y install libldap2-dev &&\
    apt-get -y install libsasl2-dev &&\
    apt-get -y install slapd &&\
    apt-get -y install ldap-utils &&\
    apt-get -y install tox &&\
    apt-get -y install lcov &&\
    apt-get -y install valgrind &&\
    apt-get install sudo
    # For intall python-ldap .....

RUN echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple/" > /etc/pip.conf &&\
    pip install --no-cache --upgrade jupyter &&\
    pip install --no-cache --upgrade jupyterlab &&\
    pip install --no-cache --upgrade python-ldap &&\
    pip install --no-cache --upgrade jupyterlab-language-pack-zh-CN

ADD /auth /srv/jupyterhub/auth
ADD /jupyterhub_config.py /srv/jupyterhub
ADD /build/health.sh /srv/jupyterhub/health.sh

RUN chmod -R 777 /home &&\
    chmod -R 777 /srv/jupyterhub/health.sh

EXPOSE 8000