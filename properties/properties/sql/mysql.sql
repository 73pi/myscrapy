mysql> create database properties;
Query OK, 1 row affected (0.01 sec)

mysql> use properties;
Database changed

mysql> create table properties(
    -> url varchar(100) not NULL,
    -> title varchar(30),
    -> comefrom varchar(30),
    -> primary key (url)
    -> );
Query OK, 0 rows affected (0.12 sec)

mysql>