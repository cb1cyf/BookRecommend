package com.rw.web;

import com.rw.pojo.User;
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

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String username = request.getParameter("name");
        User user = userService.selectByName(username);

        StringBuilder sb = new StringBuilder();
        // 拼接字符串
        // [[bookId0, score0], [bookId1, score1]...]
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

       /* System.out.println(sb);
        response.getWriter().write("test success");*/
        // 将打分放入 namenode userRatings.csv
        // 调用main.python

    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
