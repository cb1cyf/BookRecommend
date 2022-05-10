package com.rw.util;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class ExecUtil {
    public static int execBash(String arg1, String arg2, String arg3) throws InterruptedException, IOException {
        StringBuilder arg = new StringBuilder("/usr/spark-2.3.0/bin/spark-submit --jars /usr/spark-2.3.0/jars/mysql-connector-java-5.1.40/mysql-connector-java-5.1.40-bin.jar --driver-class-path /usr/spark-2.3.0/jars/mysql-connector-java-5.1.40/mysql-connector-java-5.1.40-bin.jar /usr/submit/main.py");
        arg.append(" " + arg1 + " " + arg2 + " " + arg3);

        Process pr = Runtime.getRuntime().exec(arg.toString());
        BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));
        String outputLine = "";
        while ((outputLine = in.readLine()) != null) {
            System.out.println(outputLine);
        }
        in.close();
        int status = pr.waitFor();
        if (status != 0) {
            return 1;
        }
        return status;
    }

    public static void main(String[] args) throws IOException, InterruptedException {
//        int status = execBash("Score", String.valueOf(278859), "[[11,10],[22,6],[39,7]]");
        int status = execBash("Recommend", String.valueOf(278859), "1");
        System.out.println(status);
    }
}
