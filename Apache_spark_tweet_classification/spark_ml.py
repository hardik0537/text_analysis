from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.functions import col

from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier

from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


sc =SparkContext()
sqlContext = SQLContext(sc)
data = sqlContext.read.format('com.databricks.spark.csv').options(header='false', inferschema='true').load('./data/data_final.csv')

drop_list = ['_c1', '_c2', '_c3', '_c4']
data = data.select([column for column in data.columns if column not in drop_list])


# set seed for reproducibility
(trainingData, testData) = data.randomSplit([0.7, 0.3], seed = 100)

# regular expression tokenizer
regexTokenizer = RegexTokenizer(inputCol="_c5", outputCol="words", pattern="\\W")

# stop words
add_stopwords = ["http","https","amp","rt","t","c","the"]
stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(add_stopwords)

# bag of words count
countVectors = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=10000, minDF=5)

# convert string labels to indexes
label_stringIdx = StringIndexer(inputCol = "_c0", outputCol = "label")



rfc = RandomForestClassifier(featuresCol="features", labelCol = "label", maxDepth=8, maxBins=2400000, numTrees=100)
pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, countVectors, label_stringIdx, rfc])

# Fit the pipeline to training documents.
pipelineFit = pipeline.fit(trainingData)
predictions = pipelineFit.transform(testData)
predictions.select('label', 'prediction').orderBy("probability", ascending=False).show(10)

evaluator = MulticlassClassificationEvaluator(predictionCol = "prediction",labelCol = "label", metricName = "accuracy")
print("Accuracy: %g" % (evaluator.evaluate(predictions)))
pipelineFit.save("./model/randomforest.model")