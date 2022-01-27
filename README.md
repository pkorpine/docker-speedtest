## Introduction

This is a docker image that periodically executes `speedtest` and pushes the
data to the given influxdb.

Enviromental variables:
* `INFLUXDB_HOST`: address of the influxdb service.
* `INFLUXDB_PORT`: port of the influxdb service.
* `INFLUXDB_DATABASE`: name of the database.
* `SPEEDTEST_SERVER`: Speedtest server id, use `speedtest -L to get a list of servers`.
* `TEST_INTERVAL`: Interval of the tests, in seconds.

The repo has a sample `docker-compose.yml` in a template form for Ansible etc usage.
