create database tourdb;
use tourdb;
create table users(
	u_id int auto_increment primary key,
    u_name varchar(255),
    email varchar(255) unique,
    mobno varchar(20),
    pass varchar(300),
	created_at timestamp default current_timestamp
	);
alter table users auto_increment=400001;

select * from users;

create table tour(
	t_id int auto_increment primary key,
    place varchar(250),
    tdate date,
    ttime time,
    dest varchar(250),
    tamount float
	);
alter table tour auto_increment=23001;

select * from tour;

create table hotels(
	h_id int auto_increment primary key,
    hname varchar(250),
    nodays int,
    norooms int,
    hamount float
    );
alter table hotels auto_increment=32001;

select * from hotels;

create table transactions(
	tr_id int auto_increment primary key,
    tr_uid int,
    tr_tid int,
    tr_hid int,
    total_amount float,
    p_status enum('cart','purchased','removed') default 'cart',
    foreign key (tr_uid) references users(u_id) ,
    foreign key (tr_tid) references tour(t_id),
    foreign key (tr_hid) references hotels(h_id)
    );
alter table transactions auto_increment=45001;

select * from transactions;

select * from users;

select * from tour;

select * from hotels;

select * from transactions;

select t.place,t.tdate,t.ttime,t.dest,t.tamount,h.hname,h.h_id,h.norooms,h.nodays,h.hamount, 
tr.total_amount,tr.tr_id from 
transactions tr join users u on tr.tr_uid=u.u_id
 join tour t on tr.tr_tid=t.t_id 
 join hotels h on tr.tr_hid=h.h_id
 WHERE tr.p_status='cart' AND u.u_id='400001';

SELECT t.place,t.tdate,t.ttime,t.dest,t.tamount,h.hname,h.h_id,h.hname,h.norooms,h.nodays,h.hamount,
tr.total_amount FROM transactions tr JOIN users u on tr.tr_uid=u.u_id 
JOIN tour t on tr.tr_tid=t.t_id JOIN hotels h on tr.tr_hid=h.h_id
WHERE tr.p_status='purchased' AND u.u_id='400001';
