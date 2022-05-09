package com.rw.web;

import com.alibaba.fastjson.JSON;
import com.rw.pojo.User;
import com.rw.service.UserService;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.BufferedReader;
import java.io.IOException;

@WebServlet("/checkUserValidServlet")
public class CheckUserValidServlet extends HttpServlet {
    UserService service = new UserService();
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        BufferedReader br = request.getReader();
        String params = br.readLine();//json字符串

        User user = JSON.parseObject(params, User.class);

        User user1 = service.login(user.getUserName(), user.getPassword());
        if (user1 != null) {
            response.getWriter().write("isValid");
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
