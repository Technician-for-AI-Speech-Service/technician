show databases;
select user();

create database Insa4_IOTB_final_3;
use Insa4_IOTB_final_3;

SHOW TABLES;

-- STT/TTS Table Create SQL
-- 테이블 생성 SQL - STT/TTS
CREATE TABLE STT_TTS
(
    `user_Id`       VARCHAR(12)      NOT NULL    COMMENT 'user_Id', 
    `speak_Id`      INT UNSIGNED     NOT NULL    COMMENT 'speak_Id', 
    `text_Id`       INT UNSIGNED     NOT NULL    AUTO_INCREMENT COMMENT 'text_Id', 
    `text_Content`  VARCHAR(5000)    NOT NULL    COMMENT 'text_Content', 
     PRIMARY KEY (text_Id)
);


-- Speech Table Create SQL
-- 테이블 생성 SQL - Speech
CREATE TABLE Speech
(
    `user_Id`        VARCHAR(12)      NOT NULL    COMMENT 'user_Id', 
    `speak_Id`       INT UNSIGNED     NOT NULL    AUTO_INCREMENT COMMENT 'speak_Id', 
    `speak_Content`  VARCHAR(5000)    NOT NULL    COMMENT 'speak_Content', 
     PRIMARY KEY (speak_Id),
     INDEX `idx_user_Id` (`user_Id`) -- 이 라인을 추가하여 user_Id에 인덱스를 생성합니다.
);

-- STT_TTS 테이블에 speak_Id에 대한 UNIQUE INDEX를 추가합니다.
ALTER TABLE STT_TTS
  ADD UNIQUE INDEX `idx_speak_Id` (`speak_Id`);

/*
-- Speech 테이블에 user_Id에 대한 INDEX를 추가합니다.
ALTER TABLE Speech
  ADD INDEX `idx_user_Id` (`user_Id`);
*/

-- Speech 테이블에 Foreign Key 제약 조건을 추가합니다.
ALTER TABLE Speech
  ADD CONSTRAINT `FK_Speech_speak_Id_STT_TTS_speak_Id`
  FOREIGN KEY (`speak_Id`) REFERENCES `STT_TTS` (`speak_Id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Foreign Key 삭제 SQL - Speech(speak_Id)
-- ALTER TABLE Speech
-- DROP FOREIGN KEY FK_Speech_speak_Id_STT/TTS_speak_Id;


-- User Table Create SQL
-- 테이블 생성 SQL - User
CREATE TABLE User
(
    `user_Id`          VARCHAR(12)    NOT NULL    COMMENT 'user_Id', 
    `user_Pwd`         VARCHAR(20)    NOT NULL    COMMENT 'user_Pwd', 
    `user_Name`        VARCHAR(20)    NOT NULL    COMMENT 'user_Name', 
    `user_Phone`       VARCHAR(20)    NULL        COMMENT 'user_Phone', 
    `user_Year`        YEAR           NOT NULL    COMMENT 'user_Year', 
    `user_Gender`      VARCHAR(1)     NOT NULL    COMMENT 'user_Gender', 
    `user_Disability`  VARCHAR(50)    NOT NULL    COMMENT 'user_Disability', 
    `user_Region`      VARCHAR(5)     NOT NULL    COMMENT 'user_Region', 
     PRIMARY KEY (user_Id)
);

-- Foreign Key 설정 SQL - User(user_Id) -> Speech(user_Id)
ALTER TABLE User
    ADD CONSTRAINT FK_User_user_Id_Speech_user_Id FOREIGN KEY (user_Id)
        REFERENCES Speech (user_Id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Foreign Key 삭제 SQL - User(user_Id)
-- ALTER TABLE User
-- DROP FOREIGN KEY FK_User_user_Id_Speech_user_Id;

-- First, insert into the `Speech` table.
INSERT INTO Speech (user_Id, speak_Id, speak_Content) VALUES ('admin', 1, 'Sample speech content');

-- Then, you can insert into the `User` table.
INSERT INTO User (user_Id, user_Pwd, user_Name, user_Phone, user_Year, user_Gender, user_Disability, user_Region)
VALUES ('admin', '1234', '관리자', '010-9999-9999', 2000, '남', '-', '광주');

