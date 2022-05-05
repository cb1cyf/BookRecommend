from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
import sys
import pymysql

"""
SQL Insert, Read
"""
# store register information
def InsertUser(userName, password):
    spark = SparkSession.builder.master('spark://master:7077').appName('InsertUser').getOrCreate()
    prop = {
        'user': 'root',
        'password': '12345678',
        'driver': 'com.mysql.jdbc.Driver',
        'useSSL': 'false'
    }
    userDF = spark.read.jdbc('jdbc:mysql://mysql:3306/recommend', 'user', properties=prop)
    userDF.createOrReplaceTempView('user')
    sql = "select * from user where userName='{}'".format(userName)
    sqlRes = spark.sql(sql)
    if sqlRes.count():
        print('[ERROR] Existing User Name')
        spark.stop()
        return False
    inputRDD = spark.sparkContext.parallelize(['{} {}'.format(userName, password)]).map(lambda line: line.split(' '))
    schema = StructType([
        StructField('userName', StringType(), True),
        StructField('password', StringType(), True)
    ])
    rowRDD = inputRDD.map(lambda p: Row(p[0].strip(), p[1].strip()))
    rowDF = spark.createDataFrame(rowRDD, schema)
    rowDF.write.jdbc('jdbc:mysql://mysql:3306/recommend', 'user', 'append', prop)
    print('[INFO] Insert ({}, {}) into Table user'.format(userName, password))
    spark.stop()
    return True

# delete with PyMySQL
def Delete(sql):
    conn = pymysql.connect(
        host='mysql',
        port=3306,
        user='root',
        password='12345678',
        database='recommend'
    )
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

# store recommendation
def InsertRecommend(userId, ratingList):
    # ratingList = [(bookId, rating)]
    spark = SparkSession.builder.master('spark://master:7077').appName('InsertRecommend').getOrCreate()
    prop = {
        'user': 'root',
        'password': '12345678',
        'driver': 'com.mysql.jdbc.Driver',
        'useSSL': 'false'
    }
    recommendDF = spark.read.jdbc('jdbc:mysql://mysql:3306/recommend', 'recommend', properties=prop)
    recommendDF.createOrReplaceTempView('recommend')
    sql = 'select * from recommend where userId={}'.format(userId)
    sqlRes = spark.sql(sql)
    if sqlRes.count():
        deleteSQL = 'delete from recommend where userId={}'.format(userId)
        Delete(deleteSQL)
        print('[INFO] Delete old recommendation for userId={}'.format(userId))
    inputData = ['{} {} {}'.format(userId, term[0], term[1]) for term in ratingList]
    inputRDD = spark.sparkContext.parallelize(inputData).map(lambda line: line.split(' '))
    schema = StructType([
        StructField('userId', IntegerType(), True),
        StructField('bookId', IntegerType(), True),
        StructField('rating', FloatType(), True)
    ])
    rowRDD = inputRDD.map(lambda p: Row(int(p[0]), int(p[1]), float(p[2])))
    rowDF = spark.createDataFrame(rowRDD, schema)
    rowDF.write.jdbc('jdbc:mysql://mysql:3306/recommend', 'recommend', 'append', prop)
    print('[INFO] Insert {} recommendation for userId={}'.format(len(ratingList), userId))
    spark.stop()

# login and verify
def ReadUser(userName, password):
    spark = SparkSession.builder.master('spark://master:7077').appName('ReadUser').getOrCreate()
    prop = {
        'user': 'root',
        'password': '12345678',
        'driver': 'com.mysql.jdbc.Driver',
        'useSSL': 'false'
    }
    userDF = spark.read.jdbc('jdbc:mysql://mysql:3306/recommend', 'user', properties=prop)
    userDF.createOrReplaceTempView('user')
    sql = "select * from user where userName='{}'".format(userName)
    sqlRes = spark.sql(sql)
    if not sqlRes.count():
        print('[ERROR] Wrong User Name')
        spark.stop()
        return -1
    res = sqlRes.collect()[0]
    if res['password'] != password:
        print('[ERROR] Wrong Password')
        spark.stop()
        return -2
    userId = res['userId']
    print('[INFO] User {} login with password {} and ID {}'.format(userName, password, userId))
    spark.stop()
    return userId

# show result of recommendation
def ReadRecommend(userId):
    spark = SparkSession.builder.master('spark://master:7077').appName('ReadRecommend').getOrCreate()
    prop = {
        'user': 'root',
        'password': '12345678',
        'driver': 'com.mysql.jdbc.Driver',
        'useSSL': 'false'
    }
    recommendDF = spark.read.jdbc('jdbc:mysql://mysql:3306/recommend', 'recommend', properties=prop)
    recommendDF.createOrReplaceTempView('recommend')
    sql = 'select bookId, rating from recommend where userId={}'.format(userId)
    sqlRes = spark.sql(sql).collect()
    if not len(sqlRes):
        print('[WARN] None Recommendation')
        spark.stop()
        return None
    bookDF = spark.read.jdbc('jdbc:mysql://mysql:3306/recommend', 'book', properties=prop)
    bookDF.createOrReplaceTempView('book')
    res = []
    for i in range(len(sqlRes)):
        bookId = sqlRes[i]['bookId']
        rating = sqlRes[i]['rating']
        bookSQL = 'select * from book where bookId={}'.format(bookId)
        bookRes = spark.sql(bookSQL).collect()
        if not len(bookRes):
            continue
        isbn = bookRes[0]['ISBN']
        title = bookRes[0]['title']
        author = bookRes[0]['author']
        url = bookRes[0]['url']
        res.append(tuple(bookId, isbn, title, author, url, rating))
    print('[INFO] Read {} recommendation for userId={}'.format(len(res), userId))
    spark.stop()
    return res

"""
Score, Recommend
"""
# store user score in CSV
def Score(userId, scoreList):
    # scoreList: [(bookId, score)]
    spark = SparkSession.builder.master('spark://master:7077').appName('Score').getOrCreate()
    scoreData = ['{} {} {}'.format(userId, term[0], term[1]) for term in scoreList]
    scoreRDD = spark.sparkContext.parallelize(scoreData).map(lambda line: line.split(' '))
    schema = StructType([
        StructField('userId', IntegerType(), True),
        StructField('bookId', IntegerType(), True),
        StructField('rating', FloatType(), True)
    ])
    rowRDD = scoreRDD.map(lambda p: Row(int(p[0]), int(p[1]), float(p[2])))
    rowDF = spark.createDataFrame(rowRDD, schema)
    rowDF.write.csv('hdfs://namenode:8020/input/UserRatings/', mode='append', sep=';')
    print('[INFO] Store {} score for userId={}'.format(len(scoreList), userId))
    spark.stop()

def line2row(line):
    line = line.split(';')
    row = {}
    row['userId'] = int(line[0].strip('"'))
    row['bookId'] = int(line[1].strip('"'))
    row['rating'] = float(line[2].strip('"'))
    return row

# recommend with ALS; whether training is decided by flag (train after new score)
def recommend(userId, flag):
    spark = SparkSession.builder.master('spark://master:7077').appName('ALS').getOrCreate()
    sc = spark.sparkContext
    Ratings = sc.textFile('hdfs://namenode:8020/input/Ratings.csv').zipWithIndex().filter(lambda x: x[1]>0).map(lambda line: Row(**line2row(line[0]))).toDF()
    UserRatings = sc.textFile('hdfs://namenode:8020/input/UserRatings').map(lambda line: Row(**line2row(line))).toDF()
    Ratings = Ratings.union(UserRatings)
    train, test = Ratings.randomSplit([0.8, 0.2])
    pass

if __name__ == '__main__':
    assert len(sys.argv) >= 2
    if sys.argv[1] == 'InsertUser':
        assert len(sys.argv) == 4
        flag = InsertUser(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'InsertRecommend':
        assert len(sys.argv) == 4
        InsertRecommend(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'ReadUser':
        assert len(sys.argv) == 4
        userId = ReadUser(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'ReadRecommend':
        assert len(sys.argv) == 3
        recommendResult = ReadRecommend(sys.argv[2])
    elif sys.argv[1] == 'Score':
        assert len(sys.argv) == 4
        Score(sys.argv[2], sys.argv[3])