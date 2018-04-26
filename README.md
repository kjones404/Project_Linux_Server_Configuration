# Configure A Linux Server

This project is for the Udacity Full Stack nanodegree program. The goal of this project is to a Ubuntu server to run the Item Catalog app:

The hosted app can be found [Here](http://ec2-18-216-126-4.us-east-2.compute.amazonaws.com/).

## Setting Up Your server

### 01 Getting Started

* Create your server. This server is hosted with [Amazon Lightsail](https://lightsail.aws.amazon.com/ls/webapp/home/resources).
* Once your server is created you will need to login to make updates to your server. Amazon provides a default SSH key. Using the key you cant login by typing:

ssh -i ~/.ssh/YOURSSHKEY.pem ubunut@YOURIPADDRESS

* updated your machine:

sudo apt-get update
sudo apt-get dist-upgrade

### 02 Create New User

* start by creating a new user:

adduser username

* Once the user is created update their access to sudo:

usermod -aG sudo username

### 03 Create new SSH login

* on your pc create your new ssh YOURSSHKEY

ssh-keygen

* once you have your .pub file created a new .ssh directory on your server:

mkdir .ssh

* Create an authorized keys file:

sudo nano ~/.ssh/authorized_keys

* finally restart ssh

sudo service ssh restart

### 04 Change Default SSH port

* edit the sshd config file by typeing:

sudo nano /etc/ssh/sshd_config

* change the default port 22 to your new ssh port

sudo service ssh restart

### 05 Configure Firewall

Configure your file with the requested ports:

* Make sure firewall is off

 sudo ufw status

* Deny all incoming traffic.

 sudo ufw default deny incoming

* Enable all outgoing traffic.

 sudo ufw default allow outgoing

* Allow incoming tcp packets on port 2200.

 sudo ufw allow 2200/tcp

* Allow HTTP traffic port 80.

 sudo ufw allow www

* Allow incoming udp packets on port 123.

 sudo ufw allow 123/udp

* Deny tcp and udp packets on port 22.

 sudo ufw deny 22                 

### 06 Install Apache

* run command to install Apache:

sudo apt-get install apache2

* if app is python 3

sudo apt-get install libapache2-mod-wsgi-py3

* enable wsgi

 sudo a2enmod wsgi

### 07 Install PostgreSQL

* run command to install PostgreSQL:

sudo apt-get install postgresql

* switch to the postgres user and log into psql:

sudo su - postgres

psql

* create psql user:

CREATE ROLE username WITH LOGIN PASSWORD 'password';

* give user access to create a new database:

ALTER ROLE username CREATEDB;

* exit psql and switch user

* give new user sudo

* switch back to new user, log into psql,  and create database:

createdb databasename

* exit and switch user again

### 08 Update OAuth

* add server ip to oath config and updated file paths within project

### 09 Install Item Catalog

Setup your flask application on the server. Directions can be found [Here](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04).

### 10 Restart apache and log into your server!

For additonal information please see these resources:

[How To Deploy a Flask Application on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
[boisalai](https://github.com/boisalai/udacity-linux-server-configuration/tree/master)
[adityamehra](https://github.com/adityamehra/udacity-linux-server-configuration)
