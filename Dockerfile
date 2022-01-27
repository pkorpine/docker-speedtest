FROM alpine:latest

RUN \
    apk add binutils && \
    cd /tmp && \
    wget -q https://packagecloud.io/ookla/speedtest-cli/packages/debian/bullseye/speedtest_1.1.1.28-1.c732eb82cf_amd64.deb/download.deb && \
    ar x download.deb && \
    cd / && \
    tar xvzf /tmp/data.tar.gz  && \
    rm -rf /tmp

RUN \
    apk add python3 py3-pip && \
    pip3 install influxdb

COPY speedtest_runner.py /root

CMD python3 /root/speedtest_runner.py
