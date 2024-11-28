-- MySQL Script generated by MySQL Workbench
-- Sun Oct 27 12:07:03 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema ОСББ
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema ОСББ
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ОСББ` DEFAULT CHARACTER SET utf8 ;
USE `ОСББ` ;

-- -----------------------------------------------------
-- Table `ОСББ`.`owners`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ОСББ`.`owners` (
  `idowners` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `last_name` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `phone_number` VARCHAR(45) NOT NULL,
  `e-mail` VARCHAR(45) NOT NULL,
  UNIQUE INDEX `e-mail_UNIQUE` (`e-mail` ASC) VISIBLE,
  PRIMARY KEY (`idowners`),
  UNIQUE INDEX `phone number_UNIQUE` (`phone_number` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ОСББ`.`apartments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ОСББ`.`apartments` (
  `idapartments` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `apartment_number` INT UNSIGNED NOT NULL,
  `floor` INT UNSIGNED NULL,
  `area` INT UNSIGNED NULL,
  `status` VARCHAR(45) NOT NULL,
  `idowners` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`idapartments`),
  INDEX `apar-owner_idx` (`idowners` ASC) VISIBLE,
  CONSTRAINT `apar-owner`
    FOREIGN KEY (`idowners`)
    REFERENCES `ОСББ`.`owners` (`idowners`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ОСББ`.`payments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ОСББ`.`payments` (
  `idpayments` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `idapartments` INT UNSIGNED NOT NULL,
  `payment_type` VARCHAR(45) NOT NULL,
  `sum` DECIMAL(7,2) UNSIGNED NOT NULL,
  `date` DATE NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idpayments`),
  INDEX `apartm-payments_idx` (`idapartments` ASC) VISIBLE,
  CONSTRAINT `apartm-payments`
    FOREIGN KEY (`idapartments`)
    REFERENCES `ОСББ`.`apartments` (`idapartments`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ОСББ`.`service_providers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ОСББ`.`service_providers` (
  `idservice_providers` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `service_providerscol` VARCHAR(45) NOT NULL,
  `phone_number` VARCHAR(45) NOT NULL,
  `services` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idservice_providers`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ОСББ`.`special_services_and_repairs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ОСББ`.`special_services_and_repairs` (
  `idspecial_services_and_repairs` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `services_type` VARCHAR(45) NOT NULL,
  `date_start` DATE NULL,
  `end_date` DATE NULL,
  `price` DECIMAL(8,2) UNSIGNED NOT NULL,
  `idservice providers` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`idspecial_services_and_repairs`),
  INDEX `service - providers_idx` (`idservice providers` ASC) VISIBLE,
  CONSTRAINT `service - providers`
    FOREIGN KEY (`idservice providers`)
    REFERENCES `ОСББ`.`service_providers` (`idservice_providers`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ОСББ`.`acab_director`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ОСББ`.`acab_director` (
  `idacab_director` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `took_office` DATE NULL,
  `idowners` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`idacab_director`),
  INDEX `owner-direc_idx` (`idowners` ASC) VISIBLE,
  CONSTRAINT `owner-direc`
    FOREIGN KEY (`idowners`)
    REFERENCES `ОСББ`.`owners` (`idowners`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ОСББ`.`meetings_of_the_acab`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ОСББ`.`meetings_of_the_acab` (
  `idmeetings_of_the_ACAB` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `date_start` DATE NOT NULL,
  `purpose_of_the_meeting` VARCHAR(45) NOT NULL,
  `directorid` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`idmeetings_of_the_ACAB`),
  INDEX `direct_idx` (`directorid` ASC) VISIBLE,
  CONSTRAINT `direct`
    FOREIGN KEY (`directorid`)
    REFERENCES `ОСББ`.`acab_director` (`idacab_director`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ОСББ`.`Advertisement`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ОСББ`.`Advertisement` (
  `idAdvertisement` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `theme` VARCHAR(15) NOT NULL,
  `ad_text` VARCHAR(100) NULL,
  `date_of_publication` DATE NOT NULL,
  `id_avtor` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`idAdvertisement`),
  INDEX `owner - adverisement_idx` (`id_avtor` ASC) VISIBLE,
  CONSTRAINT `owner - adverisement`
    FOREIGN KEY (`id_avtor`)
    REFERENCES `ОСББ`.`owners` (`idowners`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
