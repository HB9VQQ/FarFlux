# FarFlux

Project Goal is to facilitate the setup of a global network of [CW Beacon Monitor Stations](https://www.ncdxf.org/beacon/index.html) based on modern data storage and analytics technology to study and visualize HF Propagation paths for Amateur Radio communication.

FarFlux is a Windows utility which imports CW Beacon Logs from [Faros](http://www.dxatlas.com/Faros/) and uploads the data to an [InfluxDB](https://www.influxdata.com/) for further processing by a observability tool like [Grafana](https://grafana.com/). FarFlux validates the Faros Beacon Logs and uploads only Beacon Spots where evidence >1. The Program can be scheduled to run via the Windows Task Scheduler to upload CW Beacon Spots every 15 minutes to the database.

InfluxDB provides a <b>free</b> [cloud-hosted database](https://www.influxdata.com/products/influxdb-cloud/) with a data retention of 30 days which can be upgraded to (paid) unlimited data retention at anytime. Alternatively [InfluxDB OSS](https://docs.influxdata.com/influxdb/v2.0/get-started/#manually-download-and-install) can be installed on your own server (self-hosted) on Linux, MacOS, Docker and Kubernetes 

- If you use the cloud-hosted database provided by InfluxDB (free or paid plan) the communication port is 443 (TLS encryption)
- If you self-host the InfluxDB OSS the default communication port is 8086 (unencrypted or TLS encrypted)

Grafana is Open Source Software, available as a <b>free</b> [hosted service](https://grafana.com/products/cloud/?pg=hp&hero-sub-1-btn2) or can be downloaded and self-hosted on many different [platforms](https://grafana.com/grafana/download?pg=get&plcmt=selfmanaged-box1-cta1&edition=enterprise). An example of a CW Beacon Monitor based on InfluxDB and Grafana can be found here [CW Beacon Monitor](https://grafana.gafner.net/).


![image](https://user-images.githubusercontent.com/75934980/113480671-db95d600-9495-11eb-97ee-800ca1ad2cf6.png)

Prerequisites
=============
- Working [Faros](http://www.dxatlas.com/Faros/) installation
- Internet connection
- Admin access to a InfluxDB instance
- Admin access to a Grafana instance



Installation
============

Download the latest FarFlux Release from the dist folder and start the MSI installer file. Accept the default install path and click on Next. Once the installation is completed click on Finish.

![image](https://user-images.githubusercontent.com/75934980/114466174-65594800-9be8-11eb-9908-767105c5e979.png)

<b>Important</b> : The FarFlux Program has to be started with Admin privileges. Right-click the FarFlux Program and select "Run as administrator"




Configuration
==============
The FarFlux Software requires the configuration from your InfluxDB in order to write to the database. From "File" select "Settings" to configure FarFlux.
- InfluxDB URL (e.g. https://eu-central-1-1.aws.cloud2.influxdata.com)
- OrganizationID (e.g. MyOrg)
- Bucket (database bucket, e.g. beacon)
- Token (All Access Token for authentication)
- Port used for communication if you use a self-hosted InfluxDB (defaults to 443/TLS)

Then click on "Apply"

Example Screenshot (cloud-hosted)
-------------------
![image](https://user-images.githubusercontent.com/75934980/113779041-67755f80-972d-11eb-904d-4cf52ea0d918.png)

![image](https://user-images.githubusercontent.com/75934980/113899696-55e39480-97cd-11eb-970a-41a1b4eb9f89.png)



Windows scheduled Task
----------------------
Click on "Schedule Task" to create a windows task scheduler job which uploads the Faros beacon spots every 15 minutes to the database.

![image](https://user-images.githubusercontent.com/75934980/113900173-d7d3bd80-97cd-11eb-8f0c-425ca8cd64de.png)

![image](https://user-images.githubusercontent.com/75934980/113907126-47997680-97d5-11eb-84e6-0fb8d64c737b.png)

Once the Task has been successfully created you can safely close FarFlux (Exit), no need to keep it running. From now on the CW Beacon spots from Faros will be uploaded to the InfluxDB through the schduled Windows task every 15 minutes. Check the Data Explorer in the InfluxDB web based user interface to confirm that Beacon Spots upload is successful. Once confirmed you can go ahead with Grafana and add the Database as a Data Source to build some nice dashboards.


Grafana - adding InfluxDB as a Datasource
=========================================
Logon to your Grafana web interface and go to Configuration --> Data Sources. Click on "Add data source"
![image](https://user-images.githubusercontent.com/75934980/114545209-fa495900-9c5b-11eb-9649-805683b0a40d.png)

Select InfluxDB
![image](https://user-images.githubusercontent.com/75934980/114545484-544a1e80-9c5c-11eb-9c58-5dec070b6151.png)

Configure the Settings. Make sure you set it to the default Data Source and fill in
- URL to your InfluxDB
- Organization (OrgID from your InfluxDB)
- Token (Access token from your InfluxDB)
- Default bucket (data bucket from your InfluxDB)

Example Screenshot (cloud-hosted InfluxDB)
------------------
![image](https://user-images.githubusercontent.com/75934980/114552148-90817d00-9c64-11eb-8586-4b8f0b5e59cc.png)


Finally click on "Save & Test" to confirm successful DB connection with your provided credentials. 

If the Test has succeeded you are now ready to build Grafana dashboards. To help you get started, I have added a simple Dasboard Template to the Github Repository. You can import the Template in Grafana and all you need to change is the name of the Database bucket in each panel to reflect your setting.

Easiest way to do that, import the Template file (.json) into a text editor and search the file for "hb9cu". Replace all occurrences of "hb9cu" with your bucket name. When finished your are  ready to import the Template into Grafana.

