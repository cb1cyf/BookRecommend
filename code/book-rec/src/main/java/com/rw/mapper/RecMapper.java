package com.rw.mapper;

import com.rw.pojo.RecResult;

public interface RecMapper {
    RecResult selectByUserId(int userId);
}
