package com.rw.web;

import com.rw.pojo.User;
import com.rw.service.UserService;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/checkUserServlet")
public class CheckUserServlet extends HttpServlet {
    UserService service = new UserService();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
//        BufferedReader reader = request.getReader();
//        String s = reader.readLine();
//        System.out.println(s);
//        List<String> strings = JSON.parseArray(s, String.class);
//        System.out.println(strings);
//        User user = JSON.parseObject(s, User.class);
//        for (String string : strings) {
//            System.out.println(string);
//        }
        String username = request.getParameter("name");
        System.out.println(username);
        User selectUser = service.selectByName(username);
//        User selectUser = service.selectByName(user.getUserName());
        if (selectUser != null) {
            response.getWriter().write("exit");
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
