from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql.types import Row
from pyspark.sql import SparkSession

def line2row(line):
    line = line.split(';')
    row = {}
    row['user'] = int(line[0].strip('"'))
    row['ISBN'] = line[1].strip('"')
    row['rating'] = float(line[2].strip('"'))
    return row

spark = SparkSession.builder.master("spark://master:7077").appName("ALS").getOrCreate()
sc = spark.sparkContext
ratings = sc.textFile("hdfs://namenode:8020/input/BX-Book-Ratings.csv").zipWithIndex().filter(lambda x: x[1]>0).map(lambda line: Row(**line2row(line[0]))).toDF()
training, test = ratings.randomSplit([0.8,0.2])
alsExplicit  = ALS(maxIter=5, regParam=0.01, userCol="user", itemCol="ISBN", ratingCol="rating")
alsImplicit = ALS(maxIter=5, regParam=0.01, implicitPrefs=True,userCol="user", itemCol="ISBN", ratingCol="rating")
modelExplicit = alsExplicit.fit(training)
modelImplicit = alsImplicit.fit(training)
predictionsExplicit = modelExplicit.transform(test)
predictionsImplicit = modelImplicit.transform(test)
evaluator = RegressionEvaluator().setMetricName("rmse").setLabelCol("rating").setPredictionCol("prediction")
rmseExplicit = evaluator.evaluate(predictionsExplicit)
rmseImplicit = evaluator.evaluate(predictionsImplicit)
print("Explicit:Root-mean-square error = "+str(rmseExplicit))
print("Explicit:Root-mean-square error = "+str(rmseImplicit))

"""
apt-get update
apt-get upgrade
apt-get install gcc
apt-get install python3-dev
pip install numpy
"""