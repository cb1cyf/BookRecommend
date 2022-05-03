create table book (
    bookId int,
    ISBN varchar(20),
    title varchar(255) default NULL,
    author varchar(255) default NULL,
    url varchar(255) default NULL
);
alter table book change bookId bookId int auto_increment primary key;

