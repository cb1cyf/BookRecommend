package com.rw.web;

import com.rw.pojo.RecResult;
import com.rw.pojo.User;
import com.rw.service.RecService;
import com.rw.service.UserService;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.annotation.*;
import java.io.IOException;
import java.util.List;

@WebServlet("/checkIsHasRecResServlet")
public class CheckIsHasRecResServlet extends HttpServlet {
    RecService recService = new RecService();
    UserService userService = new UserService();


    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String username = request.getParameter("username");
        User user = userService.selectByName(username);
        List<RecResult> recResults = recService.selectByUserId(user.getUserId());
        if (recResults != null && !recResults.isEmpty()) {
            response.getWriter().write("yes");
        } else response.getWriter().write("no");
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
