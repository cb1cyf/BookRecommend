package com.rw.service;

import com.rw.mapper.RecMapper;
import com.rw.pojo.RecResult;
import com.rw.util.SqlSessionFactoryUtils;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;

public class RecService {
    SqlSessionFactory factory = SqlSessionFactoryUtils.getSqlSessionFactory();

    public RecResult selectByUserId(int userId) {
        SqlSession sqlSession = factory.openSession();
        RecMapper mapper = sqlSession.getMapper(RecMapper.class);

        RecResult recResult = mapper.selectByUserId(userId);
        sqlSession.close();
        return recResult;
    }
}
