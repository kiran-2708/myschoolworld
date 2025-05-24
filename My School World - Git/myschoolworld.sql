create database myschoolworld; 
use myschoolworld;

set sql_safe_updates=0;


create table help_desk(
ID int not null auto_increment primary key,
name varchar(255) not null,
email varchar(255) not null,
subject text not null,
message text not null
);


drop table help_desk;

select * from help_desk;


CREATE TABLE administration (
  ID INT NOT NULL UNIQUE AUTO_INCREMENT,
  school_ID VARCHAR(255) NOT NULL PRIMARY KEY,
  school_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  mobile VARCHAR(10) NOT NULL UNIQUE,
  address VARCHAR(255) NOT NULL,
  managing_director VARCHAR(255) NOT NULL,
  established_year DATE NOT NULL,
  branches INT NOT NULL,
  username VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);



insert into administration(school_ID,school_name,email,mobile,address,managing_director,established_year,
branches,username,password) values("FE20149","Vignan Scholors","kiranadigopula2708@gmail.com",
"9959575624","Hyderabad","Sunny","2019-01-01",3,"test","test");



select * from administration;

 drop table administration;



CREATE TABLE staff (
  serial_number INT NOT NULL UNIQUE AUTO_INCREMENT,
  school_ID VARCHAR(255) NOT NULL,
  staff_ID VARCHAR(255) NOT NULL PRIMARY KEY,
  staff_name VARCHAR(255) NOT NULL,
  standard VARCHAR(255) NOT NULL,
  staff_email VARCHAR(255) NOT NULL UNIQUE,
  staff_mobile VARCHAR(10) NOT NULL UNIQUE,
  username VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  qualification VARCHAR(255) NOT NULL,
  date_of_joining DATE NOT NULL,
  staff_aadhar varchar(12) not null unique,
  gender varchar(255) not null,
  FOREIGN KEY (school_ID) REFERENCES administration(school_ID) ON UPDATE CASCADE
);

 
 select * from staff;
 
 drop table staff;
 
 
 
create table staff_alumni (
 serial_number int not null primary key auto_increment,
 staff_ID varchar(255) not null,
 staff_name varchar(255) not null,
 standard varchar(255) not null,
 staff_email varchar(255) not null,
 staff_mobile varchar(10) not null,
 date_of_joining date not null,
 date_of_releaving date not null,
 gender varchar(255) not null,
 staff_aadhar varchar(255) not null
 );


select * from staff_alumni;
 
drop table staff_alumni;


 
create table student (
 serial_number int not null unique auto_increment,
 school_ID varchar(255) not null,
 staff_ID varchar(255) not null,
 student_ID varchar(255) not null primary key,
 roll_number int not null,
 student_name varchar(255) not null,
 standard varchar(255) not null,
 date_of_birth date not null,
 gender varchar(255) not null,
 student_aadhar varchar(12) not null,
 student_email varchar(255) not null,
 student_mobile varchar(255) not null,
 resident_type varchar(255) not null,
 father_name varchar(255) not null,
 father_aadhar varchar(12) not null,
 father_mobile varchar(10) not null,
 mother_name varchar(255) not null,
 mother_aadhar varchar(12) not null,
 mother_mobile varchar(10) not null,
 guardian_name varchar(255) not null,
 guardian_aadhar varchar(255) not null,
 guardian_mobile varchar(10) not null,
 relation varchar(255) not null,
 contact_email varchar(255) not null,
 address text not null,
 blood_group varchar(255) not null,
 date_of_joining date not null,
 student_username varchar(255) unique not null,
 student_password varchar(255) not null,
 username varchar(255) not null unique,
 password varchar(255) not null,
 foreign key(school_ID) references administration(school_ID) on update cascade
 );
 
 
 
drop table student;

select * from student;




create table student_alumni (
 serial_number int not null,
 school_ID varchar(255) not null,
 staff_ID varchar(255) not null,
 student_ID varchar(255) not null primary key,
 roll_number int not null,
 student_name varchar(255) not null,
 standard varchar(255) not null,
 date_of_birth date not null,
 gender varchar(255) not null,
 student_aadhar varchar(12) not null,
 student_email varchar(255) not null,
 student_mobile varchar(255) not null,
 resident_type varchar(255) not null,
 father_name varchar(255) not null,
 father_aadhar varchar(12) not null,
 father_mobile varchar(10) not null,
 mother_name varchar(255) not null,
 mother_aadhar varchar(12) not null,
 mother_mobile varchar(10) not null,
 guardian_name varchar(255) not null,
 guardian_aadhar varchar(255) not null,
 guardian_mobile varchar(10) not null,
 relation varchar(255) not null,
 contact_email varchar(255) not null,
 address text not null,
 blood_group varchar(255) not null,
 date_of_joining date not null,
 student_username varchar(255) unique not null,
 student_password varchar(255) not null,
 username varchar(255) not null unique,
 password varchar(255) not null,
 passed_out_year year not null,
 foreign key(school_ID) references administration(school_ID) on update cascade
 );
 
 
 drop table student_alumni;
 
 select * from student_alumni;
 
 
 
 create table student_alumni_results(
 id int not null unique auto_increment,
 student_ID varchar(255) not null primary key,
 student_name varchar(255) not null,
 ssc_hall_ticket varchar(255) not null unique,
 passed_out_year year not null,
 percentage decimal(5,2) not null,
 cgpa decimal(5,2) not null,
 foreign key(student_ID) references student_alumni(student_ID) on update cascade
 );
 
 drop table student_alumni_results;
 
 select * from student_alumni_results;




create table transferred_students(
ID int not null primary key auto_increment,
student_ID varchar(255) not null,
roll_number int not null,
student_name varchar(255) not null,
standard varchar(255) not null,
standard_status varchar(255) not null,
student_contact varchar(10) not null,
date_of_joining date not null,
transferred_date date not null
);


select * from transferred_students;

drop table transferred_students;


create table staff_leaves(
ID int not null auto_increment primary key,
school_ID varchar(255) not null,
staff_ID varchar(255) not null,
staff_name varchar(255) not null,
leave_type varchar(255) not null,
start_date date not null,
end_date date not null,
days int not null,
applied_on varchar(255) not null,
status varchar(255) not null default "Pending",
foreign key(school_ID) references administration(school_ID) on update cascade
);


drop table staff_leaves;

select * from staff_leaves;



create table leave_history(
ID int not null primary key,
school_ID varchar(255) not null,
staff_ID varchar(255) not null,
staff_name varchar(255) not null,
leave_type varchar(255) not null,
start_date date not null,
end_date date not null,
days int not null,
applied_on varchar(255) not null,
status varchar(255) not null,
foreign key(school_ID) references administration(school_ID) on update cascade
);


drop table leave_history;

select * from leave_history;



CREATE TABLE test_results (
    test_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(255) NOT NULL,
    roll_number int not null,
    academic_year VARCHAR(255) NOT NULL,     -- e.g. '2024-2025'
    standard VARCHAR(255) NOT NULL,
    test_name VARCHAR(255) NOT NULL,
    exam_start_date DATE NOT NULL,
    exam_end_date DATE NOT NULL,
    total_marks varchar(20) not null,
    percentage_cgpa varchar(255) not null,
    status varchar(255) not null default "Absent",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student(student_ID) ON UPDATE CASCADE
);



drop table test_results;

select * from test_results;



CREATE TABLE subject_results (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    test_id INT NOT NULL,
    date date not null,
    subject_name VARCHAR(100) NOT NULL,
    obtained_marks varchar(10) NOT NULL,
    total_marks varchar(10) NOT NULL,
    grade VARCHAR(255) not null,
    subject_status varchar(255) not null,
    FOREIGN KEY (test_id) REFERENCES test_results(test_id) ON UPDATE CASCADE
);



drop table subject_results;


select * from subject_results;




CREATE TABLE test_results_history (
    test_id INT NOT NULL PRIMARY KEY,
    student_id VARCHAR(255) NOT NULL,
    roll_number int not null,
    academic_year VARCHAR(255) NOT NULL,     -- e.g. '2024-2025'
    standard VARCHAR(255) NOT NULL,
    test_name VARCHAR(255) NOT NULL,
    exam_start_date DATE NOT NULL,
    exam_end_date DATE NOT NULL,
    total_marks varchar(20) not null,
    percentage_cgpa varchar(255) not null,
    status varchar(255) not null,
    foreign key(student_ID) references student(student_ID) on update cascade,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


drop table test_results_history;

select * from test_results_history;




CREATE TABLE subject_results_history (
    id INT NOT NULL PRIMARY KEY,
    test_id INT NOT NULL,
    date date not null,
    subject_name VARCHAR(100) NOT NULL,
    obtained_marks varchar(10) NOT NULL,
    total_marks varchar(10) NOT NULL,
    grade VARCHAR(255) not null,
    subject_status varchar(255) not null,
    FOREIGN KEY (test_id) REFERENCES test_results_history(test_id) ON UPDATE CASCADE
);


drop table subject_results_history;

select * from subject_results_history;



CREATE TABLE materials (
  id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  staff_ID varchar(255) not null,
  standard varchar(255) not null,
  file_header VARCHAR(255) NOT NULL,
  subject VARCHAR(255),
  file_name VARCHAR(255) NOT NULL,
  mime_type VARCHAR(100),
  file_data LONGBLOB NOT NULL,
  uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


drop table materials;

select * from materials;



CREATE TABLE question_papers (
  id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  staff_ID varchar(255) not null,
  standard varchar(255) not null,
  file_header VARCHAR(255) NOT NULL,
  subject VARCHAR(255),
  file_name VARCHAR(255) NOT NULL,
  mime_type VARCHAR(100),
  file_data LONGBLOB NOT NULL,
  uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



drop table question_papers;

select * from question_papers;


create table students_time_table(
	id int not null primary key auto_increment,
    standard varchar(255) not null,
	timetable_type varchar(255) not null,
    file_name varchar(255) not null,
    mime_type varchar(100) not null,
    file_data longblob not null
    );


select * from students_time_table;

drop table students_time_table;



create table staff_time_table(
	id int not null primary key auto_increment,
    staff_ID varchar(255) not null,
    file_name varchar(255) not null,
    mime_type varchar(100) not null,
    file_data longblob not null
    );

select * from staff_time_table;

drop table staff_time_table;




CREATE TABLE parents_help_desk (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parent_ID VARCHAR(255) NOT NULL,
    child_roll_number INT NOT NULL,
    child_standard VARCHAR(255) NOT NULL,
    subject VARCHAR(255),
    message TEXT,
    documents LONGBLOB,
    documents_filename TEXT,
    document_mime_type VARCHAR(255),
    audio LONGBLOB,
    audio_filename TEXT,
    audio_mime_type VARCHAR(255),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(255) NOT NULL DEFAULT "Pending"
);



drop table parents_help_desk;

select * from parents_help_desk;

