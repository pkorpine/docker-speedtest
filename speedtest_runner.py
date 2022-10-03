#!/usr/bin/env python3
import os
import time
import json
import subprocess
import logging
from influxdb import InfluxDBClient

HOST = os.getenv("INFLUXDB_HOST")
PORT = os.getenv("INFLUXDB_PORT")
DATABASE = os.getenv("INFLUXDB_DATABASE")
SPEEDTEST_SERVER = os.getenv("SPEEDTEST_SERVER")
TEST_INTERVAL = int(os.getenv("TEST_INTERVAL"))

def run_speedtest():
    cmd = f'timeout 300 speedtest --accept-license --accept-gdpr -s {SPEEDTEST_SERVER} -f json'
    logging.debug("Cmd: %s", cmd)
    output = subprocess.check_output(cmd.split(' '))
    return json.loads(output)

def push_to_influxdb(j):
    data = [
        {
            "measurement": "net",
            "tags": {
                "source": "speedtest_runner.py",
            },
            "fields": {
                "ping_jitter": j['ping']['jitter'],
                "ping_latency": j['ping']['latency'],
                "dl_bw": (8000.0 * j['download']['bytes'] / j['download']['elapsed'] / 1e6),
                "ul_bw": (8000.0 * j['upload']['bytes'] / j['upload']['elapsed'] / 1e6),
            },
        }
    ]
    client = InfluxDBClient(HOST, PORT, database=DATABASE)
    client.write_points(data)

if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)
    while True:
        t0 = time.time()
        logging.info("Running speedtest")
        data = run_speedtest()
        logging.info("Push to influxdb")
        push_to_influxdb(data)
        t1 = time.time()
        td = max(0, t1 - t0) # Protect against clock change during speedtest
        tsleep = max(0, TEST_INTERVAL - td)
        logging.info("Sleeping for %d sec", tsleep)
        time.sleep(td)
