create table user(
    userid int UNSIGNED AUTO_INCREMENT,
    uname VARCHAR(100) NOT NULL,
    passwd VARCHAR(100) NOT NULL,
    phone CHAR(11) NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY (userid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE DATABASE test;
create user 'qb'@'%' identified by  'qjbhave$';
grant all on test.* to 'qb'@'%';
flush privileges; 

conn = pymysql.connect('127.0.0.1', 'qb', 'qjbhave$', 'test')