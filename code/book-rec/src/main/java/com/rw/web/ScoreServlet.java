package com.rw.web;

import com.rw.pojo.User;
import com.rw.service.SparkService;
import com.rw.service.UserService;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Map;

@WebServlet("/scoreServlet")
public class ScoreServlet extends HttpServlet {
    UserService userService = new UserService();
    SparkService sparkService = new SparkService();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String username = request.getParameter("name");
        User user = userService.selectByName(username);

        StringBuilder sb = new StringBuilder();
        sb.append("[");
        Map<String, String[]> map = request.getParameterMap();
        for (Map.Entry<String, String[]> entry : map.entrySet()) {
            if ("name".equals(entry.getKey())) continue;
            sb.append("[");
            sb.append(entry.getKey());
            sb.append(",");
            sb.append(entry.getValue()[0]);
            sb.append("]");
            sb.append(",");
        }
        sb.deleteCharAt(sb.length() - 1);
        sb.append("]");

        String scoreList = sb.toString();
        int userId = user.getUserId();

        // 将打分放入 userRatings.csv
        // 调用main.py
        try {
            boolean status = sparkService.storeUserScoreInCSV(userId, scoreList);
            if(status) {
                response.getWriter().write("success");
                request.getRequestDispatcher("/submitServlet?userId="+userId).forward(request, response);
            } else {
                response.getWriter().write("fail");
                request.getRequestDispatcher("/error.html").forward(request, response);
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
