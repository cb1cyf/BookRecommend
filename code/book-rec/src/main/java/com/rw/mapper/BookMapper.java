package com.rw.mapper;

import com.rw.pojo.Book;

import java.util.List;

public interface BookMapper {
    Book selectById(int bookId);

    Book selectByISBN(String ISBN);

    List<Book> selectRandomTenBooks();
}
