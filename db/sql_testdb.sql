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
CREATE SCHEMA IF NOT EXISTS `test_portfolio` DEFAULT CHARACTER SET utf8 collate utf8_general_ci;
USE `test_portfolio` ;

-- -----------------------------------------------------
-- Table `portfolio`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `test_portfolio`.`user` (
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
CREATE TABLE IF NOT EXISTS `test_portfolio`.`product` (
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
    REFERENCES `test_portfolio`.`user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8 COLLATE utf8_general_ci
PACK_KEYS = Default
ROW_FORMAT = Default;


-- -----------------------------------------------------
-- Table `portfolio`.`token`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `test_portfolio`.`token` (
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
    REFERENCES `test_portfolio`.`user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8 COLLATE utf8_general_ci;


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
     set cnt = length(str)/3; 
     set i = 1; 
     set j = 1; 
     while i <=cnt DO 
           set tmpStr = substring(str,i,j); 
           set returnStr = concat(ifnull(returnStr,''), 

            case when tmpStr rlike '^(ㄱ|ㄲ)' OR ( tmpStr >= '가' AND tmpStr < '나' ) then 'ㄱ' 
                 when tmpStr rlike '^ㄴ' OR ( tmpStr >= '나' AND tmpStr < '다' ) then 'ㄴ' 
                 when tmpStr rlike '^(ㄷ|ㄸ)' OR ( tmpStr >= '다' AND tmpStr < '라' ) then 'ㄷ' 
                 when tmpStr rlike '^ㄹ' OR ( tmpStr >= '라' AND tmpStr < '마' ) then 'ㄹ' 
                 when tmpStr rlike '^ㅁ' OR ( tmpStr >= '마' AND tmpStr < '바' ) then 'ㅁ' 
                 when tmpStr rlike '^ㅂ' OR ( tmpStr >= '바' AND tmpStr < '사' ) then 'ㅂ' 
                 when tmpStr rlike '^(ㅅ|ㅆ)' OR ( tmpStr >= '사' AND tmpStr < '아' ) then 'ㅅ' 
                 when tmpStr rlike '^ㅇ' OR ( tmpStr >= '아' AND tmpStr < '자' ) then 'ㅇ' 
                 when tmpStr rlike '^(ㅈ|ㅉ)' OR ( tmpStr >= '자' AND tmpStr < '차' ) then 'ㅈ' 
                 when tmpStr rlike '^ㅊ' OR ( tmpStr >= '차' AND tmpStr < '카' ) then 'ㅊ' 
                 when tmpStr rlike '^ㅋ' OR ( tmpStr >= '카' AND tmpStr < '타' ) then 'ㅋ' 
                 when tmpStr rlike '^ㅌ' OR ( tmpStr >= '타' AND tmpStr < '파' ) then 'ㅌ' 
                 when tmpStr rlike '^ㅍ' OR ( tmpStr >= '파' AND tmpStr < '하' ) then 'ㅍ' 
            else 'ㅎ' end); 
           set i=i+1; 
     end while; 
  RETURN returnStr; 
END;