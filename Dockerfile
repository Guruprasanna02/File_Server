FROM python:latest
WORKDIR /root
RUN apt-get update > /dev/null

RUN pip3 install pycryptodome > /dev/null
RUN pip3 install mysql-connector-python > /dev/null

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