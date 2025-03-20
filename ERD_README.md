점원정보 입력
점원 아이디 Assistent_id
점원 이름 name
직책 Field2
----------------------------
발주내역 정보 입력
발주번호 Place_id
점원 아이디 Assistent_id
지출 Total_Price
날짜 Date
-----------------------------
제품발주 상세 정보 입력
제품번호 Product_id
발주번호 Place_id
제품명 Product_name
가격 price
수량 Quantity
-----------------------------
날짜 Date
매출 Sales
지출 Costs
총보유 자금 Funds

고객정보 입력
--------------
고객 아이디 Customer_id
이름 NAME 
생일 Birth 
전화번호 Phone
이메일 Email
주소 Eddress
주소 고객등급 Grade
총 지출액수 Costs 
--------------

주문내역(영수증) 입력

------------------
주문번호 Order_id
고객 아이디 customer_id
총 금액 Total_Price
점원 아이디 Assistent_id
날짜 Date
------------------


주문 상세 내역(영수증 1줄 1줄씩)

----------------
주문번호 Order_id
제품번호 Product_id
제품명 Product_name
금액 Price
수량 Quantity

----------------

진열장

-----------------
제품번호 Product_id
제품명 Product_name
바코드 Barcode
금액 Price
제고 Quantity
유통기한 Expiration_date


-- drop database convinient_store;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`convinient_store` /*!40100 DEFAULT CHARACTER SET utf8mb4 */; 

use convinient_store;

CREATE DATABASE IF NOT EXISTS convinient_store DEFAULT CHARACTER SET utf8mb4; 
USE convinient_store;

CREATE TABLE `Customers` (
	`Customer_id` INT AUTO_INCREMENT PRIMARY KEY,
	`Name` VARCHAR(10) NULL,
	`Birth` DATE NULL,
	`Phone` VARCHAR(15) NULL,
	`Email` VARCHAR(30) NULL,
	`Address` VARCHAR(30) NULL,
	`Grade` VARCHAR(6) NULL,
	`Costs` INT NULL
);

CREATE TABLE `Assistant` (
	`Assistant_id` INT AUTO_INCREMENT PRIMARY KEY,
	`Name` VARCHAR(15) NULL,
	`Field2` VARCHAR(10) NULL
);

CREATE TABLE `Daily_Account` (
	`Date` DATE NOT NULL PRIMARY KEY,
	`Sales` INT NULL,
	`Costs` INT NULL,
	`Funds` INT NULL
);

CREATE TABLE `Place_orders` (
	`Place_id` INT AUTO_INCREMENT PRIMARY KEY,
	`Assistant_id` INT NOT NULL,
	`Total_Price` INT NULL,
	`Date` DATE NOT NULL
);

CREATE TABLE `Products` (
	`Product_id` INT AUTO_INCREMENT PRIMARY KEY,
	`Product_name` VARCHAR(30) NULL,
	`Barcode` VARCHAR(13) NULL,
	`Price` INT NULL,
	`Quantity` INT NULL,
	`Expiration_date` DATE NULL
);

CREATE TABLE `Place_Order_Detail` (
	`Product_id` INT NOT NULL,
	`Place_id` INT NOT NULL,
	`Field` VARCHAR(30) NULL,
	`Field2` INT NULL,
	`Field3` INT NULL,
    PRIMARY KEY (Product_id, Place_id)
);

CREATE TABLE `Orders` (
	`Order_id` INT AUTO_INCREMENT PRIMARY KEY,
	`Customer_id` INT NOT NULL,
	`Total_Price` INT NULL,
	`Assistant_id` INT NOT NULL,
	`Date` DATE NOT NULL
);

CREATE TABLE `Order_Detail` (
	`Order_id` INT NOT NULL,
	`Product_id` INT NOT NULL,
	`Price` INT NULL,
	`Quantity` INT NULL,
    PRIMARY KEY (Order_id, Product_id)
);

ALTER TABLE Place_orders 
ADD CONSTRAINT FK_Daily_Account_Place FOREIGN KEY (`Date`) 
REFERENCES Daily_Account (`Date`);

ALTER TABLE Place_orders 
ADD CONSTRAINT FK_Assistant_Place FOREIGN KEY (Assistant_id) 
REFERENCES Assistant (Assistant_id);

ALTER TABLE Place_Order_Detail 
ADD CONSTRAINT FK_Place_Order FOREIGN KEY (Place_id) 
REFERENCES Place_orders (Place_id);

ALTER TABLE Place_Order_Detail 
ADD CONSTRAINT FK_Products_Place FOREIGN KEY (Product_id) 
REFERENCES Products (Product_id);

ALTER TABLE Orders
ADD CONSTRAINT FK_Customers_Orders FOREIGN KEY (Customer_id) 
REFERENCES Customers (Customer_id);

ALTER TABLE Orders
ADD CONSTRAINT FK_Assistant_Orders FOREIGN KEY (Assistant_id) 
REFERENCES Assistant (Assistant_id);

ALTER TABLE Orders
ADD CONSTRAINT FK_Daily_Account_Orders FOREIGN KEY (`Date`) 
REFERENCES Daily_Account (`Date`);

ALTER TABLE Order_Detail 
ADD CONSTRAINT FK_Orders_OrderDetail FOREIGN KEY (Order_id) 
REFERENCES Orders (Order_id);

ALTER TABLE Order_Detail 
ADD CONSTRAINT FK_Products_OrderDetail FOREIGN KEY (Product_id) 
REFERENCES Products (Product_id);
