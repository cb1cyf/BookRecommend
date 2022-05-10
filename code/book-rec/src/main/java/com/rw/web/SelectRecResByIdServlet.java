package com.rw.web;

import com.alibaba.fastjson.JSON;
import com.rw.pojo.Book;
import com.rw.pojo.RecResult;
import com.rw.pojo.User;
import com.rw.service.BookService;
import com.rw.service.RecService;
import com.rw.service.UserService;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@WebServlet("/selectRecResByIdServlet")
public class SelectRecResByIdServlet extends HttpServlet {
    UserService userService = new UserService();
    RecService recService = new RecService();
    BookService bookService = new BookService();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String username = request.getParameter("username");
        User user = userService.selectByName(username);

        List<RecResult> recResults = recService.selectByUserId(user.getUserId());
        List<Book> recResBooks = new ArrayList<>();
        for (RecResult recResult : recResults) {
            Integer curBookId = recResult.getBookId();
            recResBooks.add(bookService.selectById(curBookId));
        }
        String jsonString = JSON.toJSONString(recResBooks);
        response.setContentType("text/json;charset=utf-8");
        response.getWriter().write(jsonString);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
