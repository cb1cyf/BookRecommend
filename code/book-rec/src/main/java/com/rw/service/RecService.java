package com.rw.service;

import com.rw.mapper.RecMapper;
import com.rw.pojo.RecResult;
import com.rw.util.SqlSessionFactoryUtils;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;

import java.util.List;

public class RecService {
    SqlSessionFactory factory = SqlSessionFactoryUtils.getSqlSessionFactory();

    public List<RecResult> selectByUserId(int userId) {
        SqlSession sqlSession = factory.openSession();
        RecMapper mapper = sqlSession.getMapper(RecMapper.class);

        List<RecResult> recResults = mapper.selectByUserId(userId);
        sqlSession.close();
        return recResults;
    }
}
