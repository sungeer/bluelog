-- 建议：在创建数据库时统一字符集与排序规则
-- CREATE DATABASE your_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- 1) 用户表：user_account
CREATE TABLE IF NOT EXISTS user_account (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  username       VARCHAR(64)     NOT NULL COMMENT '登录名/唯一标识（小写、去空格）',
  display_name   VARCHAR(64)     NULL COMMENT '展示名（昵称）',
  password_hash  VARCHAR(255)    NOT NULL COMMENT '密码哈希（bcrypt/argon2），不存明文',
  password_salt  VARCHAR(64)     NULL COMMENT '若算法需要',
  status         TINYINT         NOT NULL DEFAULT 1 COMMENT '状态：1正常 0禁用',
  created_at     DATETIME(3)     NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '创建时间(UTC)',
  updated_at     DATETIME(3)     NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '更新时间(UTC)',
  is_deleted     TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '逻辑删除：0否 1是',
  version        INT             NOT NULL DEFAULT 0 COMMENT '乐观锁版本号',
  PRIMARY KEY (id),
  UNIQUE KEY uk_user_username (username),
  KEY idx_user_status (status)
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci
  COMMENT='用户表';


-- 2) 祝福语表：blessing
CREATE TABLE IF NOT EXISTS blessing (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '祝福语ID',
  user_id        BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  text           VARCHAR(256)    NOT NULL COMMENT '祝福语正文（建议<=120汉字）',
  status         TINYINT         NOT NULL DEFAULT 1 COMMENT '状态：1启用 0下线',
  created_at     DATETIME(3)     NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '创建时间(UTC)',
  updated_at     DATETIME(3)     NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '更新时间(UTC)',
  is_deleted     TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '逻辑删除：0否 1是',
  version        INT             NOT NULL DEFAULT 0 COMMENT '乐观锁版本号',
  PRIMARY KEY (id),
  KEY idx_user_id (user_id),
  KEY idx_blessing_status (status)
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci
  COMMENT='祝福语表';







