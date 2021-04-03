# FarFlux

FarFlux is a Windows utility which imports CW Beacon Logs from Faros http://www.dxatlas.com/Faros/ and uploads the data to an InfluxDB https://www.influxdata.com/ for further processing e.g. with Grafana. The utility validates the Faros Beacon Logs and uploads only Beacon Spots where evidence >1. The FarFlux Program can be scheduled to run via the Windows Task Scheduler like every 15Mins.

InfluxDB Cloud https://www.influxdata.com/products/influxdb-cloud/ provides a free internet hosted database with data retention of 30 days and can be upgraded to (paid) unlimited data retention. InfluxDB is Open Source Software and can be installed on your own server as well (Linux,MacOS,Docker and Kubernetes) https://docs.influxdata.com/influxdb/v2.0/get-started/#manually-download-and-install

Configuration
==============
The FarFlux Utility requires the configuration of the InfluxDB Instance name, the database bucket name and an access Token for authentication.
