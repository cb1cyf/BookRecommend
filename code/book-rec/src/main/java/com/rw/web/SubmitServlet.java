package com.rw.web;

import com.rw.service.SparkService;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/submitServlet")
public class SubmitServlet extends HttpServlet {
    SparkService sparkService = new SparkService();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String userIdStr = request.getParameter("userId");

        int userId = Integer.parseInt(userIdStr);


        try {
            boolean status = sparkService.submitComputeTaskToSpark(userId, 1);
            String contextPath = request.getContextPath();
            if (status) {
                response.sendRedirect(contextPath + "/main.html");
            } else {
                response.sendRedirect(contextPath + "/error.html");
            }
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }

    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
