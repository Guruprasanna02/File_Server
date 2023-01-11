FROM python:latest
WORKDIR /root
RUN apt-get update && apt-get install -y \
	vim \
    netcat \
    git \
    curl \
	libcurl4-openssl-dev \
    libpng-dev \
    libonig-dev \
    libxml2-dev

RUN pip3 install pycryptodome > /dev/null
RUN pip3 install mysql-connector-python > /dev/null

COPY entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh

COPY server.py /root/server.py
RUN chmod +rwx /root/server.py

COPY setupdb.py /root/setupdb.py
RUN chmod +rwx /root/setupdb.py

COPY appDev/ /root/appDev/
RUN chmod +rwx /root/appDev/

COPY webDev/ /root/webDev/
RUN chmod +rwx /root/webDev/

COPY sysAd/ /root/sysAd/
RUN chmod +rwx /root/sysAd/

CMD [ "bash", "entrypoint.sh" ]
