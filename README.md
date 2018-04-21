# Build A Item Catalog

This project is for the Udacity Full Stack nanodegree program. The goal of this project is to create an item catalog that includes:

* A JSON Endpoint
* CRUD Functionality
* Authentication

**JSON Endpoint:** Allows users to pull data from the database without any extra HTML/CSS data.

**CRUD Functionality:** includes the ability to read, create, update, and delete from the database.

**Authentication:** Utilizes Googles OAuth2.


## Before You Get Started

* This code was created using python 3.6.4. Please make sure you have the correct version of python installed before attempting to run this program. For more information on how to download python please check [Beginners Guide to Download Python](https://wiki.python.org/moin/BeginnersGuide/Download).

* This program is installed with [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and [Vagrant](https://www.vagrantup.com/downloads.html). You will need to have both installed on your computer before you can run this program without any extra modifications.

* this program requires you to save your Googles OAuth2 in a file named *"client_secrets.json"*. This file must be located in the same directory as home.py. For more information please [Click Here](https://cloud.google.com/genomics/downloading-credentials-for-api-access)  

## Getting Started

After you download the repository, you will need to update open the vagrant
folder in your command-line interface. Type *"vagrant up"* followed by *"vagrant ssh"*.

Once vagrant is up and running, navigate into your shared folder by typing *"cd /vagrant"*.

Type the following:
 * python database_setup.py
 * python load_movies.py
 * python home.py

Once *"home.py"* running. Open your browser to:
```
http://localhost:5000
```


## JSON Data

Query to pull a list of all available collections:
```
http://localhost:5000/collections/JSON
```

Query to pull a list of all movies in a collections:
```
http://localhost:5000/collections/{{collection id}}/JSON
```

Query to pull a single movie in a collections:
```
http://localhost:5000/collections/{{collection id}}/{{movie id}}/JSON
```
