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

select * from customers;


USE classicmodels;
create view cust_details as
select customerName, phone, city
from customers;

USE classicmodels;
select * from cust_details;

-- create veiws using joins
USE classicmodels;

select * from products;

-- 

USE classicmodels;
create view product_description as
SELECT productName, quantityInStock, MSRP, textDescription
FROM products as p inner join productlines as pl 
on p.productLine = pl.productLine;

--
USe classicmodels;
select * from product_description;

-- Rename the view product_description to vehicle_description
USE classicmodels;
rename table product_description
to vehicle_description;

--
USE classicmodels;
show full tables;
where Table_type = 'VIEW';

-- Drop the view vehicle_description
USE classicmodels;  
drop view if exists vehicle_description;

-- Windows Functions in SQL

USE classicmodels;
