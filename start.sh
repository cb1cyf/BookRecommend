#!/bin/bash
set -e

# root is required for docker-compose
if [ $UID -ne 0 ];then
    echo '[ERROR] Please Run as Root'
else
    echo '[INFO] Starting Containers...'
    docker-compose up -d
    echo '[INFO] Containers Started'

    # NumPy is required for PySpark ML
    echo '[INFO] Installing NumPy on Spark Master...'
    docker exec master apt-get update
    #docker exec master apt-get upgrade -y
    docker exec master apt-get install gcc -y
    docker exec master apt-get install python3-dev -y
    docker exec master pip install numpy
    echo '[INFO] NumPy Installed'

    echo '[INFO] Loading SQL Data into MySQL...'
    docker exec -i mysql sh -c 'exec mysql -uroot -p12345678 recommend' < ./SQL/book.sql
    docker exec -i mysql sh -c 'exec mysql -uroot -p12345678 recommend' < ./SQL/user.sql
    docker exec -i mysql sh -c 'exec mysql -uroot -p12345678 recommend' < ./SQL/recommend.sql
    echo '[INFO] SQL Data Loaded'

    echo '[INFO] Submitting Rating CSV File to HDFS...'
    cp ./CSV/Ratings.csv ./input_files/
    docker exec namenode hdfs dfs -mkdir /input
    docker exec namenode hdfs dfs -put /input_files/Ratings.csv /input
    echo '[INFO] File Submitted'

    echo '[INFO] Copying Code & Driver to Spark Master...'
    cp ./code/ALS.py ./submit/
    cp ./mysql-connector-java-5.1.40.tar.gz ./submit/

    echo '[INFO] Done'
fi