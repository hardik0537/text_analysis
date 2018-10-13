from pyspark.sql.functions import col
from pyspark.sql import SQLContext, SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from collections import namedtuple
from pyspark.ml import PipelineModel
import pandas as pd
# from pyspark.sql.functions import desc

sc = SparkContext("local[2]", "Streaming App")
ssc = StreamingContext(sc, 10)
sqlContext = SQLContext(sc)

socket_stream = ssc.socketTextStream("40.86.229.171", 5557) # Internal ip of  the tweepy streamer

lines = socket_stream.window(20)
fields = ("SentimentText")
Tweet = namedtuple( 'Tweet', fields )
termination_flag = 0
rf = PipelineModel.load("./model/randomforest.model")

def getSparkSessionInstance(sparkConf):
    if ("sparkSessionSingletonInstance" not in globals()):
        globals()["sparkSessionSingletonInstance"] = SparkSession \
            .builder \
            .config(conf=sparkConf) \
            .getOrCreate()
    return globals()["sparkSessionSingletonInstance"]

def rdd_iterator(time, rdd):
    try:
        
        print("========= %s =========" % str(time))
        
        # Get the singleton instance of SparkSession
        print("in try")
        spark = getSparkSessionInstance(rdd.context.getConf())
        print("spark session")
        # Convert RDD[String] to RDD[Tweet] to DataFrame
        rowRdd = rdd.map(lambda w: Tweet(w))
        linesDataFrame = spark.createDataFrame(rowRdd)
        print("linesDataframe created.")
        # Creates a temporary view using the DataFrame
        linesDataFrame.createOrReplaceTempView("tweets")
    
        # Do tweet character count on table using SQL and print it
        lineCountsDataFrame = spark.sql("select SentimentText as _c5 from tweets")
        print("before prediction")
        prediction = rf.transform(lineCountsDataFrame)
        print("after prediction")
        #prediction.show()
        keep_list = ["_c5", "prediction"]
        prediction_save = prediction.select([column for column in prediction.columns if column in keep_list])
        pred = prediction_save.toPandas()
        pred.to_csv('./data/output_data/output.csv', mode='a', header=False, index = False)
        
        tweets_in_csv = pd.read_csv('./data/output_data/output.csv', index_col = False, encoding = 'unicode_escape')
        if (len(tweets_in_csv)> 100):
            ssc.stop()
    except:
        print("terminate")
        
    

# key part!

lines.foreachRDD(rdd_iterator)

ssc.start()
ssc.awaitTermination()
