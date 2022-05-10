package com.rw.service;

import com.rw.util.ExecUtil;

import java.io.IOException;

public class SparkService {

    /**
     * store user score in CSV
     *
     * @param userId
     * @param scoreList: [[userId0, score0],[userId1, score1],...]
     * @return
     * @throws IOException
     * @throws InterruptedException
     */
    public boolean storeUserScoreInCSV(int userId, String scoreList) throws IOException, InterruptedException {
        int status = ExecUtil.execBash("Score", String.valueOf(userId), scoreList);
        return status == 0;
    }

    /**
     * submit task to spark cluster
     * @param userId
     * @param flag: 1->train 0->not train
     * @return
     * @throws IOException
     * @throws InterruptedException
     */
    public boolean submitComputeTaskToSpark(int userId, int flag) throws IOException, InterruptedException {
        int status = ExecUtil.execBash("Recommend", String.valueOf(userId), String.valueOf(flag));
        return status == 0;
    }

//    public static void main(String[] args) throws IOException, InterruptedException {
//        boolean status = submitComputeTaskToSpark(278859, 1);
//        System.out.println(status);
//    }
}
