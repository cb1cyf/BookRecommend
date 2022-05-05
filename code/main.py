from pyspark.sql import SparkSession
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
    sql = f"select * from user where userName='{userName}'"
    sqlRes = spark.sql(sql)
    if sqlRes.count():
        print('[ERROR] Existing User Name')
        spark.stop()
        return False
    inputRDD = spark.sparkContext.parallelize([f'{userName} {password}']).map(lambda line : line.split(' '))
    schema = StructType([
        StructField('userName', StringType(), True),
        StructField('password', StringType(), True)
    ])
    rowRDD = inputRDD.map(lambda p : Row(p[0].strip(), p[1].strip()))
    rowDF = spark.createDataFrame(rowRDD, schema)
    rowDF.write.jdbc('jdbc:mysql://mysql:3306/recommend', 'user', 'append', prop)
    print(f'[INFO] Insert ({userName}, {password}) into Table user')
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

# store result of recommendation
def InsertRecommend(userId, bookId, rating):
    spark = SparkSession.builder.master('spark://master:7077').appName('InsertRecommend').getOrCreate()
    prop = {
        'user': 'root',
        'password': '12345678',
        'driver': 'com.mysql.jdbc.Driver',
        'useSSL': 'false'
    }
    recommendDF = spark.read.jdbc('jdbc:mysql://mysql:3306/recommend', 'recommend', properties=prop)
    recommendDF.createOrReplaceTempView('recommend')
    sql = f'select * from recommend where userId={userId}'
    sqlRes = spark.sql(sql)
    if sqlRes.count():
        deleteSQL = f'delete from recommend where userId={userId}'
        Delete(deleteSQL)
    inputRDD = spark.sparkContext.parallelize([f'{userId} {bookId} {rating}']).map(lambda line : line.split(' '))
    schema = StructType([
        StructField('userId', IntegerType(), True),
        StructField('bookId', IntegerType(), True),
        StructField('rating', FloatType(), True)
    ])
    rowRDD = inputRDD.map(lambda p : Row(int(p[0]), int(p[1]), float(p[2])))
    rowDF = spark.createDataFrame(rowRDD, schema)
    rowDF.write.jdbc('jdbc:mysql://mysql:3306/recommend', 'recommend', 'append', prop)
    print(f'[INFO] Insert ({userId}, {bookId}, {rating}) into Table recommend')
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
    sql = f"select * from user where userName='{userName}'"
    sqlRes = spark.sql(sql)
    if not sqlRes.count():
        print('[ERROR] Wrong User Name')
        spark.stop()
        return None
    res = sqlRes.collect()[0]
    if res['password'] != password:
        print('[ERROR] Wrong Password')
        spark.stop()
        return None
    userId = res['userId']
    print(f'[INFO] User {userName} Login with Password {password} and ID {userId}')
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
    sql = f'select bookId, rating from recommend where userId={userId}'
    sqlRes = spark.sql(sql).collect()
    if not len(sqlRes):
        print('[WARN] None Recommend Result')
        spark.stop()
        return None
    bookDF = spark.read.jdbc('jdbc:mysql://mysql:3306/recommend', 'book', properties=prop)
    bookDF.createOrReplaceTempView('book')
    res = []
    for i in range(len(sqlRes)):
        bookId = sqlRes[i]['bookId']
        rating = sqlRes[i]['rating']
        bookSQL = f'select * from book where bookId={bookId}'
        bookRes = spark.sql(bookSQL).collect()
        if not len(bookRes):
            continue
        isbn = bookRes[0]['ISBN']
        title = bookRes[0]['title']
        author = bookRes[0]['author']
        url = bookRes[0]['url']
        res.append(tuple(bookId, isbn, title, author, url, rating))
    return res

if __name__ == '__main__':
    assert len(sys.argv) >= 2
    if sys.argv[1] == 'InsertUser':
        assert len(sys.argv) == 4
        flag = InsertUser(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'InsertRecommend':
        assert len(sys.argv) == 5
        InsertRecommend(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'ReadUser':
        assert len(sys.argv) == 4
        userId = ReadUser(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'ReadRecommend':
        assert len(sys.argv) == 3
        recommendResult = ReadRecommend(sys.argv[2])