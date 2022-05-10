package com.rw.web;

import com.rw.pojo.User;
import com.rw.service.UserService;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.annotation.*;
import java.io.IOException;

@WebServlet("/loginServlet")
public class LoginServlet extends HttpServlet {
    UserService service = new UserService();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String username = request.getParameter("username");
        String password = request.getParameter("password");

        User user = service.login(username, password);
        String contextPath = request.getContextPath();
        if (user != null) {
            // 重定向
            response.sendRedirect(contextPath + "/main.html");
        } else {
            response.sendRedirect(contextPath + "/login.html");
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
