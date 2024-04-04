use nptel_management;

show full processlist;

kill 209;



DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS teacher;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS register_course;
DROP TABLE IF EXISTS certificate;
DROP TABLE IF EXISTS NPTEL_MARKS;
DROP TABLE IF EXISTS Ad_min;
DROP TABLE IF EXISTS set_course;

create table STUDENT(
dig_id TEXT,
regno INTEGER,
st_name TEXT,
dob DATE,
gender TEXT,
dept TEXT,
section TEXT,
email_id VARCHAR(100) primary key,
sem TEXT,
acc_year TEXT,
pass_word TEXT
);

create table TEACHER(
staffname TEXT,
email_id VARCHAR(100) Primary key,
pass_word Text
);

create table Course(
c_code VARCHAR(15) PRIMARY KEY,
c_name TEXT,
weeks INTEGER,
nptel_link varchar(255),
if_yes VARCHAR(5)
);

create table REGISTER_COURSE(
email_id varchar(255),
c_code varchar(25),
PRIMARY KEY (EMAIL_ID,C_CODE)
);

create table certificate(
email_id varchar(255),
c_code Varchar(25),
marks INTEGER,
certificate_data LONGBLOB NOT NULL,
verified varchar(10),
qr_code_url varchar(255),
PRIMARY KEY (EMAIL_ID,C_CODE)
);

create table NPTEL_MARKS(
email_id  varchar(255),
c_code varchar(20),
verified_marks integer,
ssn_marks integer,
PRIMARY KEY (EMAIL_ID,C_CODE)
);

create table Ad_min(
email_id varchar(255) PRIMARY KEY
);

create Table set_course(
c_no INTEGER PRIMARY KEY AUTO_INCREMENT,
SEM VARCHAR(10),
DEPT VARCHAR(10),
C_CODE VARCHAR(10),
ACC_YEAR varchar(15)
);

Insert into STUDENT values ('D1234', 1001, 'Rahul Sharma', '1999-05-15', 'Male', 'Information Technology', 'A', 'rahul.sharma@ssn.edu.in', '3', '2024-2025', 'rahulpass123');
Insert into STUDENT values ('D5678', 1002, 'Priya Patel', '2000-02-28', 'Female', 'Computer Science', 'B', 'priya.patel@ssn.edu.in', '4', '2023-2024', 'priyapass456');
Insert into STUDENT values ('D9012', 1003, 'Amit Singh', '1998-11-10', 'Male', 'Electronics and Communication', 'C', 'amit.singh@ssn.edu.in', '5', '2022-2023', 'amitpass789');
Insert into STUDENT values ('D3456', 1004, 'Ananya Das', '2001-08-05', 'Female', 'Computer Engineering', 'A', 'ananya.das@ssn.edu.in', '2', '2025-2026', 'ananyapass1234');
Insert into STUDENT values ('D7890', 1005, 'Rajesh Kumar', '1997-04-20', 'Male', 'Mechanical Engineering', 'B', 'rajesh.kumar@ssn.edu.in', '6', '2021-2022', 'rajeshpass567');

Insert into TEACHER values ('Dr. Gupta', 'gupta@ssn.edu.in', 'teacherpass123');
Insert into TEACHER values ('Prof. Singh', 'singh@ssn.edu.in', 'faculty456pass');
Insert into TEACHER values ('Ms. Sharma', 'sharma@ssn.edu.in', 'pass789teacher');
Insert into TEACHER values ('Dr. Patel', 'patel@ssn.edu.in', 'drexelprof');
Insert into TEACHER values ('Prof. Khan', 'khan@ssn.edu.in', 'profpass987');

Insert into Course values ('IT101', 'Database Management Systems', 12, 'https://nptel.com/it101', 'Yes');
Insert into Course values ('CS201', 'Data Structures and Algorithms', 10, 'https://nptel.com/cs201', 'No');
Insert into Course values ('ECE301', 'Digital Signal Processing', 14, 'https://nptel.com/ece301', 'Yes');
Insert into Course values ('CE401', 'Software Engineering', 16, 'https://nptel.com/ce401', 'No');
Insert into Course values ('ME501', 'Mechatronics', 8, 'https://nptel.com/me501', 'Yes');

Insert into REGISTER_COURSE values ('rahul.sharma@ssn.edu.in', 'IT101');
Insert into REGISTER_COURSE values ('priya.patel@ssn.edu.in', 'ECE301');
Insert into REGISTER_COURSE values ('amit.singh@ssn.edu.in', 'CE401');
Insert into REGISTER_COURSE values ('ananya.das@ssn.edu.in', 'CS201');
Insert into REGISTER_COURSE values ('rajesh.kumar@ssn.edu.in', 'ME501');



Insert into NPTEL_MARKS values ('rahul.sharma@ssn.edu.in', 'IT101', 80, 75);
Insert into NPTEL_MARKS values ('priya.patel@ssn.edu.in', 'ECE301', 90, 85);
Insert into NPTEL_MARKS values ('amit.singh@ssn.edu.in', 'CE401', 75, 70);
Insert into NPTEL_MARKS values ('ananya.das@ssn.edu.in', 'CS201', 88, 82);
Insert into NPTEL_MARKS values ('rajesh.kumar@ssn.edu.in', 'ME501', 82, 78);

Insert into Ad_min values ('admin@ssn.edu.in');

Insert into set_course (SEM, DEPT, C_CODE, ACC_YEAR) values ('3', 'IT', 'IT101', '2024-2025');
Insert into set_course (SEM, DEPT, C_CODE, ACC_YEAR) values ('4', 'IT', 'CS201', '2023-2024');
Insert into set_course (SEM, DEPT, C_CODE, ACC_YEAR) values ('5', 'IT', 'ECE301', '2022-2023');
Insert into set_course (SEM, DEPT, C_CODE, ACC_YEAR) values ('6', 'IT', 'CE401', '2025-2026');
Insert into set_course (SEM, DEPT, C_CODE, ACC_YEAR) values ('7', 'IT', 'ME501', '2021-2022');
Insert into set_course (SEM, DEPT, C_CODE, ACC_YEAR) values ('3', 'IT', 'ME501', '2021-2022');

(select sem from student where email_id = 'rahul.sharma@ssn.edu.in');
select c.c_name from course c
join set_course s on c.c_code = s.c_code
where sem = (select sem from student where email_id = 'rahul.sharma@ssn.edu.in');


select c.c_code,c.c_name,weeks,nptel_link,dept,acc_year from course c
join set_course s on c.c_code = s.c_code
where c.c_name = 'Database Management Systems';

select s.st_name, s.sem, c.c_name, ce.marks from student s
join certificate ce on ce.email_id = s.email_id
join course c on c.c_code = ce.c_code;

select n.email_id,s.st_name, c.c_name, n.verified_marks 
from nptel_marks n
join student s on s.email_id = n.email_id
join course c on c.c_code = n.c_code;

select * from certificate;

