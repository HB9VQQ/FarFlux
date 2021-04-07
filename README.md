# FarFlux

FarFlux is a Windows utility which imports CW Beacon Logs from Faros http://www.dxatlas.com/Faros/ and uploads the data to an InfluxDB https://www.influxdata.com/ for further processing by a observability tool like Grafana https://grafana.com/. FarFlux validates the Faros Beacon Logs and uploads only Beacon Spots where evidence >1. The Program can be scheduled to run via the Windows Task Scheduler like every 15Mins.

InfluxDB provides a <b>free</b> cloud-hosted database https://www.influxdata.com/products/influxdb-cloud/ with a data retention of 30 days which can be upgraded to (paid) unlimited data retention at anytime. Alternatively InfluxDB OSS can be installed on your own server (self-hosted) on Linux, MacOS, Docker and Kubernetes https://docs.influxdata.com/influxdb/v2.0/get-started/#manually-download-and-install

- If you use the cloud-hosted database provided by InfluxDB (free or paid plan) the communication port is 443 (TLS encryption)
- If you self-host the InfluxDB OSS the default communication port is 8086 (unencrypted or TLS encrypted)

Grafana is Open Source Software, available as a <b>free</b> hosted service https://grafana.com/products/cloud/?pg=hp&hero-sub-1-btn2 or can be downloaded and self-hosted on many different platforms https://grafana.com/grafana/download?pg=get&plcmt=selfmanaged-box1-cta1&edition=enterprise. An example of a CW Beacon Monitor can be found here https://grafana.gafner.net/ (registration required).


![image](https://user-images.githubusercontent.com/75934980/113480671-db95d600-9495-11eb-97ee-800ca1ad2cf6.png)


Configuration
==============
The FarFlux Utility requires the configuration from your InfluxDB in order to write to the database:
- InfluxDB URL (e.g. https://eu-central-1-1.aws.cloud2.influxdata.com)
- OrganizationID (e.g. MyOrg)
- Bucket (database bucket, e.g. beacon)
- Token (All Access Token for authentication)
- Port used for communication if you use a self-hosted InfluxDB (defaults to 443/TLS)

Then click on "Apply"

Example Screenshot (cloud-hosted)
-------------------
![image](https://user-images.githubusercontent.com/75934980/113779041-67755f80-972d-11eb-904d-4cf52ea0d918.png)

![image](https://user-images.githubusercontent.com/75934980/113707087-b1375900-96df-11eb-8e1b-792219e05323.png)


Windows scheduled Task
----------------------
Click on "Schedule Upload Task" to create a windows task scheduler job which uploads the Faros beacon spots every 15 minutes to the database.

![image](https://user-images.githubusercontent.com/75934980/113707888-d5476a00-96e0-11eb-8a24-7b10b41c9a99.png)



