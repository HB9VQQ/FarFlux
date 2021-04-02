# FarFlux

FarFlux is a Windows utility which imports CW Beacon Logs from Faros http://www.dxatlas.com/Faros/ and uploads the data to an InfluxDB https://www.influxdata.com/ for further processing e.g. with Grafana. The utility validates the Faros Beacon Logs and uploads only Data where evidence >1. The FarFlux Program can be scheduled to run via the Windows Task Scheduler like every 15Mins.

Configuration
==============
The FarFlux Utility requires the configuration of the InluxDB Instance name the database bucket name and an access Token for authentication.
