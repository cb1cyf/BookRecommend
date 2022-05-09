package com.rw.service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class SparkService {
    /*store user score in CSV*/
    public void storeUserScoreInCSV(int userId, String scoreList) throws IOException, InterruptedException {
        /*docker exec master \
/usr/spark-2.3.0/bin/spark-submit \
--jars /usr/spark-2.3.0/jars/mysql-connector-java-5.1.40/mysql-connector-java-5.1.40-bin.jar \
--driver-class-path /usr/spark-2.3.0/jars/mysql-connector-java-5.1.40/mysql-connector-java-5.1.40-bin.jar \
/usr/submit/main.py \
func func_arg1 func_arg2*/
        System.out.println(System.getProperty("user.dir"));
        String arg1 = "arg1";
        String arg2 = "arg2";
        String[] arg = new String[]{"python", "./main.py", arg1, arg2};
        Process pr = Runtime.getRuntime().exec(arg);
        BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));
        String line;
        while ((line=in.readLine()) != null) {
            System.out.println(line);
        }
        in.close();
        System.out.println("end1");
        pr.waitFor();
    }

    public static void main(String[] args) throws IOException, InterruptedException {
        System.out.println(System.getProperty("user.dir"));
//        String arg1 = "Score";
//        String arg2 = "278859";
//        String arg3 = "[[1,2],[2,4],[3,5]]";
//        String[] arg = new String[]{"docker exec master /usr/spark-2.3.0/bin/spark-submit --jars /usr/spark-2.3.0/jars/mysql-connector-java-5.1.40/mysql-connector-java-5.1.40-bin.jar --driver-class-path /usr/spark-2.3.0/jars/mysql-connector-java-5.1.40/mysql-connector-java-5.1.40-bin.jar /usr/submit/main.py",arg1, arg2, arg3};
//        String[]arg = new String[]{"python", "/Users/lhy/workspace/Bigdata/BookRecommend/code/book-rec/src/main/java/com/rw/service/main.py"};
//        String arg = "docker exec master \\\n" +
//                "/usr/spark-2.3.0/bin/spark-submit \\\n" +
//                "--jars /usr/spark-2.3.0/jars/mysql-connector-java-5.1.40/mysql-connector-java-5.1.40-bin.jar \\\n" +
//                "--driver-class-path /usr/spark-2.3.0/jars/mysql-connector-java-5.1.40/mysql-connector-java-5.1.40-bin.jar \\\n" +
//                "/usr/submit/main.py \\\n" +
//                "Score 278859 [[1,2],[2,4],[3,5]]";
//        String arg = "python /Users/lhy/workspace/Bigdata/BookRecommend/code/book-rec/src/main/java/com/rw/service/main.py";
        String arg = "node -v";
        Process pr = Runtime.getRuntime().exec(arg);
        BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));
        String line;
        while ((line=in.readLine()) != null) {
            System.out.println(line);
        }
        in.close();
//        System.out.println("end1");
        pr.waitFor();
    }
}
