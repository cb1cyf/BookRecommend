create table recommend (
    userId int,
    bookId int,
    rating float,
    primary key (userId, bookId)
);