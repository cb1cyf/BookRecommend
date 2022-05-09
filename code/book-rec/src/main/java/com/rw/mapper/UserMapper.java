package com.rw.mapper;

import com.rw.pojo.User;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface UserMapper {

    /**FLAG 仅作测试 注意删除
     * 选择所有用户
     * @return
     */
    List<User> selectAll();

    /**
     * 根据用户名查询用户
     * @param userName
     * @return User
     */
    User selectByName(@Param("name") String userName);

    /**
     * 根据用户名和密码查询用户
     * @param userName
     * @param password
     * @return User
     */
    User select(@Param("username") String userName, @Param("password") String password);

    /**
     * 新增用户
     * @param username
     * @param password
     */
    void add(@Param("username") String username, @Param("password") String password);

}
