package com.rw.service;

import com.rw.mapper.BookMapper;
import com.rw.pojo.Book;
import com.rw.util.SqlSessionFactoryUtils;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;

import java.util.List;

public class BookService {
    SqlSessionFactory factory = SqlSessionFactoryUtils.getSqlSessionFactory();

    public Book selectById(int bookId) {
        SqlSession sqlSession = factory.openSession();
        BookMapper mapper = sqlSession.getMapper(BookMapper.class);

        Book book = mapper.selectById(bookId);
        sqlSession.close();
        return book;
    }

    public Book selectByISBN(String ISBN) {
        SqlSession sqlSession = factory.openSession();
        BookMapper mapper = sqlSession.getMapper(BookMapper.class);

        Book book = mapper.selectByISBN(ISBN);
        sqlSession.close();
        return book;
    }
    public List<Book> selectRandomTenBooks() {
        SqlSession sqlSession = factory.openSession();
        BookMapper mapper = sqlSession.getMapper(BookMapper.class);

        List<Book> books = mapper.selectRandomTenBooks();
        sqlSession.close();
        return books;
    }
}
