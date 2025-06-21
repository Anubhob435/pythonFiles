USE classicmodels;


select productCode, productName, MSRP from products
where productCode in(
    select productCode from orderdetails
    where priceEach < 100
    );

