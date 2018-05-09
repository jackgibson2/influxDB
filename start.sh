#!/bin/bash

docker run -d -p 8086:8086 --name=influxdb --net=influxdb influxdb
docker run -p 8888:8888 --name=chronograf --net=influxdb chronograf --influxdb-url=http://influxdb:8086 &
