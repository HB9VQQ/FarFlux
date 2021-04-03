# FarFlux

FarFlux is a Windows utility which imports CW Beacon Logs from Faros http://www.dxatlas.com/Faros/ and uploads the data to an InfluxDB https://www.influxdata.com/ for further processing e.g. Grafana. The utility validates the Faros Beacon Logs and uploads only Beacon Spots where evidence >1. The FarFlux Program can be scheduled to run via the Windows Task Scheduler like every 15Mins.

InfluxDB Cloud https://www.influxdata.com/products/influxdb-cloud/ provides a free internet hosted database with data retention of 30 days and can be upgraded to (paid) unlimited data retention. InfluxDB is Open Source Software and can be installed on your own server as well (Linux,MacOS,Docker and Kubernetes) https://docs.influxdata.com/influxdb/v2.0/get-started/#manually-download-and-install


![image](https://user-images.githubusercontent.com/75934980/113480671-db95d600-9495-11eb-97ee-800ca1ad2cf6.png)


Configuration
==============
The FarFlux Utility requires the configuration from InfluxDB in order to write to the database:
- InfluxDB URL (e.g. https://eu-central-1-1.aws.cloud2.influxdata.com)
- OrganizationID (e.g. beacon_mon)
- Bucket (e.g. faros_spots)
- Token (authentication token)
