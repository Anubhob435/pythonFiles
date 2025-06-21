-- SQL query to find products with price under 100
USE classicmodels;

select productCode, productName, MSRP from products
where productCode in(
    select productCode from orderdetails
    where priceEach < 100
);
-- SQL query to create a stored procedure to find products with price under 100
delimiter //
create procedure getProductsUnder100()
begin
    select productCode, productName, MSRP from products
    where productCode in(
        select productCode from orderdetails
        where priceEach < 100
    );
end;

call getProductsUnder100();

-- SQL query to find employees

USE classicmodels;
select * from employees;

-- select all payments made by customers

USE classicmodels;
select * from payments 
ORDER BY amount DESC;

-- dillimitor to find all male employees
USE employees;

delimiter //
create procedure getMaleEmployees()
begin
    select * from employees
    where gender = 'M'
    Limit 1000;
end;

-- SQL query
USE employees;
call getMaleEmployees();

--

-- TRIGGERS IN SQL
use sql_intro;

create table Student
(st_roll int, age int, name varchar(30), marks float);

create trigger marks_verify
before insert on Student
for each row 
begin
    if new.marks < 0 then 
        set new.marks = 50;
    end if;
end;

--
USE sql_intro;

INSERT INTO Student (st_roll, age, name, marks) VALUES
(1, 20, 'John Smith', 85.5),
(2, 19, 'Emily Johnson', 92.0),
(3, 21, 'Michael Brown', 78.5),
(4, 20, 'Sarah Davis', -10),
(5, 22, 'David Wilson', 88.0),
(6, 19, 'Lisa Anderson', 95.5),
(7, 20, 'James Taylor', 82.0),
(8, 21, 'Emma Martinez', 89.5),
(9, 19, 'Robert Garcia', 76.0),
(10, 20, 'Olivia Rodriguez', -5);

-- checking the trigger
USE sql_intro;
select * from Student;

-- to drop trigger
drop trigger if exists marks_verify;

--
USE classicmodels;

