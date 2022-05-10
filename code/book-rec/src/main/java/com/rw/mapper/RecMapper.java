package com.rw.mapper;

import com.rw.pojo.RecResult;

import java.util.List;

public interface RecMapper {
    List<RecResult> selectByUserId(int userId);
}
