create sequence signup_seq start 3001 increment by 1 no cycle
create table signup(u_id int DEFAULT (nextval('signup_seq')) unique primary key not null,
username varchar(50) not null,u_dob date not null,u_emailid varchar(60) unique not null,
u_password varchar(256) not null,u_phno varchar(10) not null,u_gender varchar(10) not null)
select * from signup
drop table signup
drop sequence signup_seq
--delete from signup where u_id=3005

create table admin(id serial unique primary key not null,adminname varchar(50),adminpass varchar(50))
insert into admin(adminname,adminpass) values('Reshma','resh')
select * from admin
drop table admin

create sequence doctor_seq start 4001 increment by 1 no cycle
create table doctor(doc_id int DEFAULT (nextval('doctor_seq')) unique primary key not null,
docname varchar(50) not null,specialist varchar(50) not null,doc_emailid varchar(60) not null,
doc_phno varchar(10) not null,doc_addr varchar(50) not null,doc_gender varchar(10) not null,
doc_num varchar(5) not null,doc_expr integer not null)
select * from doctor
drop table doctor
drop sequence doctor_seq

--d_date text default (current_date || ' ' || to_char(current_timestamp,'HH:MI:SS'))not null

create table dhistory(dhis_id serial primary key,preg integer not null,glucose integer not null,
bp integer not null,skinthick integer not null,insulin integer not null,weight real not null,
height real not null,pedigree varchar(50) not null,age integer not null,d_result varchar(15) not null,
u_id int references signup(u_id) not null,d_date text not null)
select * from dhistory
drop table dhistory

create table lhistory(lhis_id serial primary key,gender varchar(10) not null,age integer not null,
smoking varchar(5) not null,yellow_fingers varchar(5) not null,anxiety varchar(5) not null,
peer_pressure varchar(5) not null,chronic_disease varchar(5) not null,fatigue varchar(5) not null,
allergy varchar(5) not null,wheezing varchar(5) not null,alcohol varchar(5) not null,
coughing varchar(5) not null,shortness_of_breath varchar(5) not null,
swallowing_difficulty varchar(5) not null,chest_pain varchar(5) not null,l_result varchar(15) not null,
u_id int references signup(u_id) not null,l_date text not null)
select * from lhistory
drop table lhistory

create table hearthistory(hhis_id serial primary key,age integer not null,
sex varchar(10) not null,chestpaintype varchar(10) not null,restingbp integer not null,
cholesterol integer not null,fastingbs varchar(5) not null,restingecg varchar(10) not null,
maxhr integer not null,exerciseangina varchar(5) not null,oldpeak real not null,
st_slope varchar(10) not null,h_result varchar(15) not null,
u_id int references signup(u_id) not null,h_date text not null)
select * from hearthistory
drop table hearthistory

create table shistory(shis_id serial primary key,gender varchar(10) not null,
age integer not null,hypertension varchar(5) not null,
heart_disease varchar(5) not null,ever_married varchar(15) not null,
work_type varchar(20) not null,residence_type varchar(10) not null,
avg_glucose_level real not null,weight real not null,height real not null,
smoking_status varchar(20) not null,s_result varchar(15) not null,
u_id int references signup(u_id) not null,s_date text not null)
select * from shistory
drop table shistory

create sequence feed_seq start 5001 increment by 1 no cycle
create table feedback(f_id int DEFAULT (nextval('feed_seq')) unique primary key not null,
rating integer not null,f_message varchar(300) not null,u_id int references signup(u_id) not null)
select * from feedback
drop table feedback
drop sequence feed_seq

create sequence appo_seq start 6001 increment by 1 no cycle
create table appointment(appo_id int DEFAULT (nextval('appo_seq')) unique primary key not null,
appo_date text not null,appo_time text not null,pat_name varchar(50) not null,pat_age integer not null,
pat_sympt varchar(50) not null,pat_phno varchar(10) not null,doc_name varchar(50) not null,
doc_specialist varchar(50) not null,doc_phno varchar(10) not null,doc_addr varchar(50) not null,
u_id int references signup(u_id) not null,doc_id int references doctor(doc_id) not null)
select * from appointment
drop table appointment
drop sequence appo_seq