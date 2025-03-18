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