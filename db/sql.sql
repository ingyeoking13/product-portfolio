-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema portfolio
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema portfolio
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `portfolio` DEFAULT CHARACTER SET utf8 collate utf8_general_ci;
USE `portfolio` ;

-- -----------------------------------------------------
-- Table `portfolio`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `portfolio`.`user` (
  `id` VARCHAR(36) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL,
  `cell_number` VARCHAR(64) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NULL DEFAULT NULL,
  `password` VARCHAR(64) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id` (`id` ASC),
  INDEX `ix_user_cell_number` (`cell_number` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8 COLLATE utf8_general_ci
PACK_KEYS = Default;


-- -----------------------------------------------------
-- Table `portfolio`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `portfolio`.`product` (
  `id` VARCHAR(36) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL,
  `category` VARCHAR(36) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL COMMENT '카테고리',
  `price` FLOAT NOT NULL COMMENT '가격',
  `raw_price` FLOAT NOT NULL COMMENT '원가',
  `name` VARCHAR(36) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL COMMENT '이름',
  `description` TEXT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL COMMENT '설명',
  `barcode` TEXT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL COMMENT '바코드',
  `expiration_date` DATETIME NOT NULL COMMENT '유통기한',
  `size` VARCHAR(36) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL COMMENT '사이즈',
  `snowflake_id` VARCHAR(100) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL COMMENT '스노우플레이크 ID/커서용',
  `deleted_at` DATETIME NULL DEFAULT NULL,
  `user_id` VARCHAR(36) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC),
  INDEX `ix_product_category` (`category` ASC),
  FULLTEXT (name, description) WITH PARSER ngram,
  CONSTRAINT `product_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `portfolio`.`user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8 COLLATE utf8_general_ci
PACK_KEYS = Default
ROW_FORMAT = Default;


-- -----------------------------------------------------
-- Table `portfolio`.`token`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `portfolio`.`token` (
  `id` VARCHAR(36) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL,
  `access_token` VARCHAR(300) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `deleted_at` DATETIME NULL DEFAULT NULL,
  `user_id` VARCHAR(36) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC),
  INDEX `ix_token_access_token` (`access_token` ASC),
  CONSTRAINT `token_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `portfolio`.`user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8 COLLATE utf8_general_ci;


INSERT INTO user (id, cell_number, password) VALUES
('a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8', '010-1234-5678', '$2b$12$MZ.KB428S1tYkl9M9Oyyz.0ag3MZqAxO9aNxBYlB8nhtAm9RvGB5y'),
('b2c3d4e5-f6g7-8901-h2i3-j4k5l6m7n8o9', '010-2345-6789', '$2b$12$MZ.KB428S1tYkl9M9Oyyz.0ag3MZqAxO9aNxBYlB8nhtAm9RvGB5y'),
('c3d4e5f6-g7h8-9012-i3j4-k5l6m7n8o9p0', '010-3456-7890', '$2b$12$MZ.KB428S1tYkl9M9Oyyz.0ag3MZqAxO9aNxBYlB8nhtAm9RvGB5y'),
('d4e5f6g7-h8i9-0123-j4k5-l6m7n8o9p0q1', '010-4567-8901', '$2b$12$MZ.KB428S1tYkl9M9Oyyz.0ag3MZqAxO9aNxBYlB8nhtAm9RvGB5y'),
('e5f6g7h8-i9j0-1234-k5l6-m7n8o9p0q1r2', '010-5678-9012', '$2b$12$MZ.KB428S1tYkl9M9Oyyz.0ag3MZqAxO9aNxBYlB8nhtAm9RvGB5y');
-- password : pass1234


INSERT INTO product (id, category, price, raw_price, name, description, barcode, expiration_date, size, snowflake_id, deleted_at, user_id) VALUES
('a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n1', 'cat001', 10000, 12000, '과자', '이 상품은 맛있는 과자로, 건강에 좋은 재료만을 사용하여 만들어졌습니다. 아이들 간식이나 파티 음식으로 적합합니다.', '1234567890123', '2024-12-31', '중', 'aaaa', NULL, 'a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8'),
('a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n2', 'cat002', 20000, 22000, '음료', '이 상품은 고급 음료로서, 세계 각국에서 공수한 최상급 원료로 제조되었습니다. 건강과 맛을 동시에 챙길 수 있는 선택입니다.', '1234567890124', '2025-01-31', '대', 'bbb', NULL, 'a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8'),
('a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n3', 'cat003', 15000, 17000, '바나나', '이 상품은 신선한 과일로, 자연 그대로의 맛과 영양을 제공합니다. 유기농으로 재배되어 안전하고 건강한 먹거리를 보장합니다.', '1234567890125', '2024-06-30', '소', 'ccc', NULL, 'a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8'),
('a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n4', 'cat003', 15000, 17000, '슈크림 라떼', '이 상품은 신선한 과일로, 자연 그대로의 맛과 영양을 제공합니다. 유기농으로 재배되어 안전하고 건강한 먹거리를 보장합니다.', '1234567890125', '2024-06-30', '소', 'ddd', NULL, 'a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8'),
('a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n5', 'cat003', 15000, 17000, '샤인머스켓', '이 상품은 신선한 과일로, 자연 그대로의 맛과 영양을 제공합니다. 유기농으로 재배되어 안전하고 건강한 먹거리를 보장합니다.', '1234567890125', '2024-06-30', '소', 'eee', NULL, 'a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8'),
('a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n6', 'cat003', 15000, 17000, '파인애플', '이 상품은 신선한 과일로, 자연 그대로의 맛과 영양을 제공합니다. 유기농으로 재배되어 안전하고 건강한 먹거리를 보장합니다.', '1234567890125', '2024-06-30', '소', 'fff', NULL, 'e5f6g7h8-i9j0-1234-k5l6-m7n8o9p0q1r2'),
('a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7a1', 'cat003', 15000, 17000, '샤샤', '이 상품은 신선한 과일로, 자연 그대로의 맛과 영양을 제공합니다. 유기농으로 재배되어 안전하고 건강한 먹거리를 보장합니다.', '1234567890125', '2024-06-30', '소', 'ggg', NULL, 'e5f6g7h8-i9j0-1234-k5l6-m7n8o9p0q1r2');


CREATE FUNCTION `fn_choSearch`(`str` varchar(200)) RETURNS varchar(200) CHARSET utf8 
BEGIN 
     declare returnStr varchar(200); 
     declare cnt int; 
     declare i int; 
     declare j int; 
     declare tmpStr varchar(200); 

     if str is null then 
         return ''; 
     end if; 

     set str = replace(str, ' ', '');
     set i = 1; 
     while i <=length(str) DO 
           set tmpStr = substring(str,i,1); 
           set returnStr = concat(ifnull(returnStr,''), 

            case when ( tmpStr >= '가' AND tmpStr < '나' ) then 'ㄱ' 
                 when ( tmpStr >= '나' AND tmpStr < '다' ) then 'ㄴ' 
                 when ( tmpStr >= '다' AND tmpStr < '라' ) then 'ㄷ' 
                 when ( tmpStr >= '라' AND tmpStr < '마' ) then 'ㄹ' 
                 when ( tmpStr >= '마' AND tmpStr < '바' ) then 'ㅁ' 
                 when ( tmpStr >= '바' AND tmpStr < '사' ) then 'ㅂ' 
                 when ( tmpStr >= '사' AND tmpStr < '아' ) then 'ㅅ' 
                 when ( tmpStr >= '아' AND tmpStr < '자' ) then 'ㅇ' 
                 when ( tmpStr >= '자' AND tmpStr < '차' ) then 'ㅈ' 
                 when ( tmpStr >= '차' AND tmpStr < '카' ) then 'ㅊ' 
                 when ( tmpStr >= '카' AND tmpStr < '타' ) then 'ㅋ' 
                 when ( tmpStr >= '타' AND tmpStr < '파' ) then 'ㅌ' 
                 when ( tmpStr >= '파' AND tmpStr < '하' ) then 'ㅍ' 
            else 'ㅎ' end); 
           set i=i+1; 
     end while; 
  RETURN returnStr; 
END;