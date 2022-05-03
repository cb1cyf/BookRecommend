from pyspark.sql import SparkSession
from pyspark.sql.types import Row, StructType, StructField, StringType, IntegerType

spark = SparkSession.builder.master("spark://master:7077").appName("TrySQL").getOrCreate()
studentRDD = spark.sparkContext.parallelize(["5 Rongcheng M 16","6 Guanhua M 17"]).map(lambda line : line.split(" "))
schema = StructType([StructField("name", StringType(), True),StructField("gender", StringType(), True),StructField("age",IntegerType(), True)])
rowRDD = studentRDD.map(lambda p : Row(p[1].strip(), p[2].strip(),int(p[3])))
studentDF = spark.createDataFrame(rowRDD, schema)
prop = {}
prop['user'] = 'root'
prop['password'] = '12345678'
prop['driver'] = "com.mysql.jdbc.Driver"
studentDF.write.jdbc("jdbc:mysql://mysql:3306/recommend",'student','append', prop)
#spark.stop()

'''
./bin/spark-submit --jars /usr/spark-2.3.0/jars/mysql-connector-java-5.1.40/mysql-connector-java-5.1.40-bin.jar \
--driver-class-path /usr/spark-2.3.0/jars/mysql-connector-java-5.1.40/mysql-connector-java-5.1.40-bin.jar \
../code.py 
'''

"""
import os
path = './BX-SQL-Dump/BX-Users.sql'
f = open(path, 'r', encoding='ISO-8859-1')
sql = f.readlines()
f.close()
print(len(sql))
"""