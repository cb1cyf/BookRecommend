package com.rw.web;

import com.rw.pojo.User;
import com.rw.service.UserService;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.annotation.*;
import java.io.IOException;

@WebServlet("/registerServlet")
public class RegisterServlet extends HttpServlet {
    UserService service = new UserService();
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String username = request.getParameter("username");
        String password = request.getParameter("password");
        User user = new User();
        user.setUserName(username);
        user.setPassword(password);

        boolean regStatus = service.register(user);
        if (regStatus) {
//            response.getWriter().write("success");
            request.getRequestDispatcher("/login.html").forward(request, response);
        } else {
            request.getRequestDispatcher("/register.html").forward(request, response);
        }

    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
