create table user (
    userId int,
    userName varchar(50) default NULL,
    password varchar(50) default NULL
);
alter table user change userId userId int auto_increment primary key;
alter table user auto_increment=278859;