# 기초 잡기

1. 제품정보

1) 제품 id
2) 바코드
3) 제품명
4) 가격
5) 수량
6) 유통기한


2. 제품 목록

products = [
    ("제품 ID", "EAN-13 바코드", "제품명", "가격", "수량", "유통기한"),
    (1, "8801234567890", "참치 삼각김밥", 1500, 50, "2024-03-20"),
    (2, "8801234567891", "불고기 삼각김밥", 1500, 45, "2024-03-20"),
    (3, "8801234567892", "치킨 도시락", 4500, 30, "2024-03-21"),
    (4, "8801234567893", "제육볶음 도시락", 4500, 25, "2024-03-21"),
    (5, "8801234567894", "신라면 컵", 2000, 60, "2024-09-10"),
    (6, "8801234567895", "진라면 컵", 1800, 50, "2024-09-10"),
    (7, "8801234567896", "불닭볶음면 컵", 2200, 40, "2024-09-10"),
    (8, "8801234567897", "생수 (500ml)", 1000, 100, "2025-03-10"),
    (9, "8801234567898", "생수 (2L)", 2000, 80, "2025-03-10"),
    (10, "8801234567899", "콜라 (500ml)", 2500, 70, "2025-03-10"),
    (11, "8801234567800", "사이다 (500ml)", 2500, 65, "2025-03-10"),
    (12, "8801234567801", "캔커피", 2200, 50, "2025-03-10"),
    (13, "8801234567802", "아메리카노 PET", 3500, 40, "2024-09-10"),
    (14, "8801234567803", "초코우유 (300ml)", 2000, 55, "2024-03-30"),
    (15, "8801234567804", "바나나우유 (300ml)", 2200, 50, "2024-03-30"),
    (16, "8801234567805", "햄치즈 샌드위치", 3500, 30, "2024-03-20"),
    (17, "8801234567806", "참치마요 샌드위치", 3500, 28, "2024-03-20"),
    (18, "8801234567807", "새우깡", 1500, 60, "2024-09-10"),
    (19, "8801234567808", "포테이토칩", 1800, 55, "2024-09-10"),
    (20, "8801234567809", "가나 초콜릿", 2500, 45, "2025-03-10")
]

(`id`,`barcode`,`product_name`,`price`,`quantity`,`expiration_day`)
("제품 ID", "EAN-13 바코드", "제품명", "가격", "수량", "유통기한")

------------------------------------------------------------------------
# 쿼리문 작성

/*
*********************************************************************
http://www.mysqltutorial.org
*********************************************************************
Name: MySQL Sample Database for Python
Link: http://www.mysqltutorial.org/
Version 1.1
*********************************************************************
*/
-- drop database convinient_store;
/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`convinient_store` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `convinient_store`;
CREATE TABLE `products` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `barcode` varchar(13) NOT NULL,
  `product_name` varchar(30) NOT NULL,
  `price` int NOT NULL,
  `quantity` int NOT NULL,
  `expiration_day` date NOT NULL,
  
  UNIQUE KEY `barcode` (`barcode`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `products` */
insert  into `products`(`barcode`,`product_name`,`price`,`quantity`,`expiration_day`) values 
(8801234567890, "참치 삼각김밥", 1500, 50, "2024-03-20"),
(8801234567891, "불고기 삼각김밥", 1500, 45, "2024-03-20"),
(8801234567892, "치킨 도시락", 4500, 30, "2024-03-21"),
(8801234567893, "제육볶음 도시락", 4500, 25, "2024-03-21"),
(8801234567894, "신라면 컵", 2000, 60, "2024-09-10"),
(8801234567895, "진라면 컵", 1800, 50, "2024-09-10"),
(8801234567896, "불닭볶음면 컵", 2200, 40, "2024-09-10"),
(8801234567897, "생수 (500ml)", 1000, 100, "2025-03-10"),
(8801234567898, "생수 (2L)", 2000, 80, "2025-03-10"),
(8801234567899, "콜라 (500ml)", 2500, 70, "2025-03-10"),
(8801234567800, "사이다 (500ml)", 2500, 65, "2025-03-10"),
(8801234567801, "캔커피", 2200, 50, "2025-03-10"),
(8801234567802, "아메리카노 PET", 3500, 40, "2024-09-10"),
(8801234567803, "초코우유 (300ml)", 2000, 55, "2024-03-30"),
(8801234567804, "바나나우유 (300ml)", 2200, 50, "2024-03-30"),
(8801234567805, "햄치즈 샌드위치", 3500, 30, "2024-03-20"),
(8801234567806, "참치마요 샌드위치", 3500, 28, "2024-03-20"),
(8801234567807, "새우깡", 1500, 60, "2024-09-10"),
(8801234567808, "포테이토칩", 1800, 55, "2024-09-10"),
(8801234567809, "가나 초콜릿", 2500, 45, "2025-03-10");
    
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

----------------------------------------------------------------------------

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
