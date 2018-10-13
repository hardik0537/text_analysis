#  Classification through Apache Spark streaming using Twitter data

Performing streaming of the real time data from social media platform (Twitter) by using the big data analytical tool (Apache Spark). Apply machine learning techniques (classification algorithms) to the streamed data to predict .

### Installation

Installation steps are for Ubuntu 16.04 version.


#### Installation of pacakges on python 3.x.x
Python is pre-installed on the server instance. You can check it by the below command:
```sh
$python3 -V
```
If python is not installed, here is the link to install python3.x on ubuntu - [Python3.x.x installation](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04)

1. Installing pip package:
```sh
$ sudo apt-get install -y python-pip
```
2. Install pyspark:
```sh
$ pip install pyspark  
```
3. Install pandas:
```sh
$ pip install pandas  
```
4. Install Tweepy:
```sh
$ pip install tweepy  
```
Now the environment is ready.
### Assuming the spark is installed on the server as per the given instructions in the tutorial.

### Running the commands:
Before running it, all the three files should be in same dir.
* First create few dirs at home:
```sh
$ mkdir data
$ mkdir data/output_data
$ mkdir model
```

* Keep the tarining CSV-file in ./data path.

* Now start the spark as per the instrction given in the tutorial.
* Run the first program
```sh
$SPARK_HOME/bin/spark-submit spark_ml.py
```
* Now open another session for the server in another terminal and run the tweepy_stream.py file.
  * Note: if it gives bind error: please change the host which is define in the main function of the file
```sh
python tweepy_stream.py
```
* Once, it prints Listening, from another terminal, run the following command:
```sh
$SPARK_HOME/bin/spark-submit spark_predict_output.py
```

Finally, the output csv file will be saved in the path "data/output_data" as output.csv
