# Sentiment Analysis of Twitter Tweet Data using ETL Process and Elastic Search

The main purpose of this assignment is to perform the sentimental analysis by understanding the extracting, transforming and loading the data process into NoSQL database. Furthermore, this processed data is analyzed using basic machine learning algorithm.

### Installation

Installation steps are for Ubuntu 16.04 version.

##### Installation steps the Elastic Search
1. Add the pre-requisite software JAVA PPA to apt-run:

```sh
$ sudo add-apt-repository -y ppa:webupd8team/java
$ sudo apt-get update
$ sudo apt-get -y install oracle-java8-installer
```
2. Download and install the public signing key:
```sh
$ swget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
```

3. Save the definition of the repository to /etc/apt/sources.list.d/elasticsearch-6.x.list:
```
$ echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list
```
4.  Install elasticsearch
```sh
$ sudo apt-get install elasticsearch
```
5.  Some important config changes:
```sh
$ sudo vim /etc/elasticsearch/elasticsearch.yml
```
* Locate and uncomment node.name and cluster.name and give new names.
* Locate and uncomment network.host and change to 0.0.0.0.
* Save the file and exit.
6. Restart the elasticsearch service
```sh
$ sudo service elasticsearch restart
```
7. Test elastic search is running:
```sh
$ sudo service elasticsearch status
```
The elastic search is ready to use. You can use any REST client (Postman, Insomia, Kibana, etc.) for doing the CRUD (Create, Read, Update and Delete) operations.

#### Installation of pacakges on python 2.7.x
Python is pre-installed on the server instance. You can check it by the below command:
```sh
$python2 -V
```
If python 2 is not installed, here is the link to install python2.7 on ubuntu - [Python2.7x installation](https://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/)

1. Installing pip package:
```sh
$ sudo apt-get install -y python2-pip
```
2. Install numpy:
```sh
$ pip2 install numpy  
```
3. Install pandas:
```sh
$ pip2 install pandas  
```

4. Install Tweepy:
```sh
$ pip2 install tweepy  
```

5. Install ElasticSearch Dsl package 
```sh
$ pip install elasticsearch-dsl  
```
Now the environment is ready.

### Running the batch script requirements:

The required files to successfully run the batch script are: <br />

| Filename      | Purpose       |
| ------------- | ------------- |
| lexicons_easy.csv      | Lexicons csv file used as train set for the model |
| EC.py      | Responsible for extracting and transforming the data      |
| sentiment_analysis.py | Responsible for analysing the data ans store it in csv file   |
| load_elasticsearch.py | Responsible for inserting the data in elastic search database |
| ETLprocess.sh | Automation script for running all the above python files   |

These all files are files should be in the same dir as the script lies in. The script name is **ETLprocess.sh**

Thus it is required that all the files including the scripts should be in the same dir to run the script successfully.

