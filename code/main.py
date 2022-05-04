from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
import sys

def InsertUser(userName, password):
    spark = SparkSession.builder.master("spark://master:7077").appName("InsertUser").getOrCreate()
    inputRDD = spark.sparkContext.parallelize([f'{userName} {password}']).map(lambda line : line.split(' '))
    schema = StructType([
        StructField('userName', StringType(), True),
        StructField('password', StringType(), True)
    ])
    rowRDD = inputRDD.map(lambda p : Row(p[0].strip(), p[1].strip()))
    rowDF = spark.createDataFrame(rowRDD, schema)
    prop = {
        'user': 'root',
        'password': '123456878',
        'driver': 'com.mysql.jdbc.Driver'
    }
    rowDF.write.jdbc('jdbc:mysql://mysql:3306/recommend', 'user', 'append', prop)
    spark.stop()

def InsertRecommend(userId, bookId, rating):
    spark = SparkSession.builder.master("spark://master:7077").appName("InsertRecommend").getOrCreate()
    inputRDD = spark.sparkContext.parallelize([f'{userId} {bookId} {rating}']).map(lambda line : line.split(' '))
    schema = StructType([
        StructField('userId', IntegerType(), True),
        StructField('bookId', IntegerType(), True),
        StructField('rating', FloatType(), True)
    ])
    rowRDD = inputRDD.map(lambda p : Row(int(p[0]), int(p[1]), float(p[2])))
    rowDF = spark.createDataFrame(rowRDD, schema)
    prop = {
        'user': 'root',
        'password': '123456878',
        'driver': 'com.mysql.jdbc.Driver'
    }
    rowDF.write.jdbc('jdbc:mysql://mysql:3306/recommend', 'recommend', 'append', prop)
    spark.stop()

if __name__ == '__main__':
    len(sys.argv)