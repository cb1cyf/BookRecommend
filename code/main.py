from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import lit
from pyspark.sql.types import *
from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder, CrossValidatorModel
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

# parse list arg
def parser(strList):
    # strList: [[bookId, rating]]; type: str
    strList = strList.split(',')
    l = len(strList)
    res = []
    for i in range(0, l, 2):
        bookId = int(strList[i].strip('[').strip(']'))
        rating = float(strList[i+1].strip('[').strip(']'))
        res.append((bookId, rating))
    return res

# store recommendation
def InsertRecommend(userId, ratingList):
    # ratingList = [[bookId, rating]]; typ: str
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
    ratingList = parser(ratingList)
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
    sqlRes = spark.sql(sql)
    if not sqlRes.count():
        print('[WARN] None Recommendation')
        spark.stop()
        return None
    bookDF = spark.read.jdbc('jdbc:mysql://mysql:3306/recommend', 'book', properties=prop)
    resDF = sqlRes.join(bookDF, 'bookId', 'inner')
    """
    res = []
    def f(row):
        res.append((row['bookId'], row['ISBN'], row['title'], row['author'], row['url'], row['rating']))
    resDF.foreach(f)
    """
    resRDD = resDF.collect()
    res = []
    for row in resRDD:
        res.append([row['bookId'], row['ISBN'], row['title'], row['author'], row['url'], row['rating']])
    print('[INFO] Read {} recommendation for userId={}'.format(len(res), userId))
    spark.stop()
    return res

"""
Score, Recommend
"""
def line2row(line):
    line = line.split(';')
    row = {}
    row['userId'] = int(line[0].strip('"'))
    row['bookId'] = int(line[1].strip('"'))
    row['rating'] = float(line[2].strip('"'))
    return row

# random select 10 books which have not been scored by userId
def Book(userId):
    spark = SparkSession.builder.master('spark://master:7077').appName('Book').getOrCreate()
    sc = spark.sparkContext
    UserRatings = sc.textFile('hdfs://namenode:8020/input/UserRatings').map(lambda line: Row(**line2row(line))).toDF()
    UserRatings.createOrReplaceTempView('UserRatings')
    sql = 'select bookId from UserRatings where userId={}'.format(userId)
    userBook = spark.sql(sql)
    prop = {
        'user': 'root',
        'password': '12345678',
        'driver': 'com.mysql.jdbc.Driver',
        'useSSL': 'false'
    }
    bookDF = spark.read.jdbc('jdbc:mysql://mysql:3306/recommend', 'book', properties=prop)
    bookIdDF = bookDF.select('bookId').subtract(userBook)
    frac = 15.0 / bookIdDF.count()
    candidate = bookIdDF.sample(frac).take(10)
    bookDF.createOrReplaceTempView('bookDF')
    bookIds = [row['bookId'] for row in candidate]
    bookRes = bookDF[bookDF.bookId.isin(bookIds)].collect()
    res = []
    for row in bookRes:
        res.append([row['bookId'], row['ISBN'], row['title'], row['author'], row['url']])
    print('[INFO] {} book to be scored for userId={}'.format(len(res), userId))
    spark.stop()
    return res

# store user score in CSV
def Score(userId, scoreList):
    # scoreList: [[bookId, score]]; type: str
    spark = SparkSession.builder.master('spark://master:7077').appName('Score').getOrCreate()
    scoreList = parser(scoreList)
    scoreData = ['{} {} {}'.format(userId, term[0], term[1]) for term in scoreList]
    scoreRDD = spark.sparkContext.parallelize(scoreData).map(lambda line: line.split(' '))
    schema = StructType([
        StructField('userId', IntegerType(), True),
        StructField('bookId', IntegerType(), True),
        StructField('rating', FloatType(), True)
    ])
    rowRDD = scoreRDD.map(lambda p: Row(int(p[0]), int(p[1]), float(p[2])))
    rowDF = spark.createDataFrame(rowRDD, schema)
    rowDF.write.csv('hdfs://namenode:8020/input/UserRatings', mode='append', sep=';')
    print('[INFO] Store {} score for userId={}'.format(len(scoreList), userId))
    spark.stop()

# recommend with ALS; whether training is decided by flag (train after new score)
def Recommend(userId, flag):
    # flag: 1 = train; 0 = not train
    spark = SparkSession.builder.master('spark://master:7077').appName('ALS').getOrCreate()
    sc = spark.sparkContext
    UserRatings = sc.textFile('hdfs://namenode:8020/input/UserRatings').map(lambda line: Row(**line2row(line))).toDF()
    if flag == '1':
        Ratings = sc.textFile('hdfs://namenode:8020/input/Ratings.csv').zipWithIndex().filter(lambda x: x[1]>0).map(lambda line: Row(**line2row(line[0]))).toDF()
        dataset = Ratings.union(UserRatings)
        """
        als = ALS(userCol='userId', itemCol='bookId', ratingCol='rating')
        paramGrid = ParamGridBuilder().addGrid(als.rank, list(range(10, 21, 2))).addGrid(als.maxIter, [10, 20, 30]).addGrid(als.regParam, [i/10.0 for i in range(1, 11)]).build()
        evaluator = RegressionEvaluator(predictionCol='prediction', labelCol='rating', metricName='rmse')
        cv = CrossValidator(estimator=als, estimatorParamMaps=paramGrid, evaluator=evaluator)
        cvALS = cv.fit(dataset)
        bestALS = cvALS.bestModel
        bestALS.write().overwrite().save('/usr/model')
        """
        als = ALS(rank=10, maxIter=10, regParam=0.1, userCol='userId', itemCol='bookId', ratingCol='rating')
        model = als.fit(dataset)
        # ISSUE: save on HDFS instead of local path like '/usr/model'
        # https://stackoverflow.com/questions/41881191/empty-collection-error-when-trying-to-load-a-saved-spark-model-using-pyspark
        # https://stackoverflow.com/questions/40327379/why-cant-i-load-a-pyspark-randomforestclassifier-model
        model.write().overwrite().save('hdfs://namenode:8020/input/model')
    else:
        model = ALSModel.load('hdfs://namenode:8020/input/model')
    UserRatings.createOrReplaceTempView('UserRatings')
    sql = 'select bookId from UserRatings where userId={}'.format(userId)
    userBook = spark.sql(sql)
    prop = {
        'user': 'root',
        'password': '12345678',
        'driver': 'com.mysql.jdbc.Driver',
        'useSSL': 'false'
    }
    bookDF = spark.read.jdbc('jdbc:mysql://mysql:3306/recommend', 'book', properties=prop).select('bookId')
    candidate = bookDF.subtract(userBook)
    candidate = candidate.withColumn('userId', lit(int(userId))).withColumn('rating', lit(0.0))
    prediction = model.transform(candidate).select('bookId', 'prediction').fillna(-1).filter('prediction>0')
    resRowList = prediction.sort('prediction', ascending=False).take(10)
    """
    res = []
    def f(row):
        res.append((row['bookId'], row['prediction']))
    resDF.foreach(f)
    """
    res = []
    for row in resRowList:
        res.append([row['bookId'], row['prediction']])
    print('[INFO] {} recommendation by ALS for userId={}'.format(len(res), userId))
    InsertRecommend(userId, res)
    spark.stop()
    return res


"""
Command:
docker exec master \
/usr/spark-2.3.0/bin/spark-submit \
--jars /usr/spark-2.3.0/jars/mysql-connector-java-5.1.40/mysql-connector-java-5.1.40-bin.jar \
--driver-class-path /usr/spark-2.3.0/jars/mysql-connector-java-5.1.40/mysql-connector-java-5.1.40-bin.jar \
/usr/submit/main.py \
func func_arg1 func_arg2
"""


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
    elif sys.argv[1] == 'Book':
        assert len(sys.argv) == 3
        bookList = Book(sys.argv[2])
    elif sys.argv[1] == 'Score':
        assert len(sys.argv) == 4
        Score(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'Recommend':
        assert len(sys.argv) == 4
        assert sys.argv[3] in ['0', '1']
        res = Recommend(sys.argv[2], sys.argv[3])