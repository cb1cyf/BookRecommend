package com.rw.sparklauncher;

import org.apache.spark.launcher.SparkAppHandle;
import org.apache.spark.launcher.SparkLauncher;

import java.io.IOException;

public class Demo {
    public static void main(String[] args) throws IOException {
        Process sl = new SparkLauncher()
                .setMaster("172.18.0.8")
                .addPyFile("main.py")
                .addAppArgs()
                .launch();
    }
}
