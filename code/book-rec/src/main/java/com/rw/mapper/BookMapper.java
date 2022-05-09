package com.rw.mapper;

import com.rw.pojo.Book;

public interface BookMapper {
    Book selectById(int bookId);

    Book selectByISBN(String ISBN);
}
