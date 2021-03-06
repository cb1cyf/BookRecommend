package com.rw.service;

import com.rw.mapper.UserMapper;
import com.rw.pojo.User;
import com.rw.util.SqlSessionFactoryUtils;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;


public class UserService {
    SqlSessionFactory factory = SqlSessionFactoryUtils.getSqlSessionFactory();

    public User selectByName(String userName) {
        SqlSession sqlSession = factory.openSession();
        UserMapper mapper = sqlSession.getMapper(UserMapper.class);

        User user = mapper.selectByName(userName);
        sqlSession.close();
        return user;
    }

    public User login(String username, String password) {
        SqlSession sqlSession = factory.openSession();
        UserMapper mapper = sqlSession.getMapper(UserMapper.class);

        User user = mapper.select(username, password);
        sqlSession.close();
        return user;
    }

    public boolean register(User user) {
        SqlSession sqlSession = factory.openSession();
        UserMapper mapper = sqlSession.getMapper(UserMapper.class);

        User userRes = mapper.selectByName(user.getUserName());
        if (userRes == null) {
            mapper.add(user.getUserName(), user.getPassword());
            sqlSession.commit();
        }
        sqlSession.close();
        return userRes == null;
    }

    public void add(String username, String password) {
        SqlSession sqlSession = factory.openSession();
        UserMapper mapper = sqlSession.getMapper(UserMapper.class);

        mapper.add(username, password);
        // 不要忘记提交事务
        sqlSession.commit();

        sqlSession.close();
        return;
    }

}
