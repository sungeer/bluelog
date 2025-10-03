


CREATE TABLE `user` (
    `id` INT(10) NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(20) NOT NULL COMMENT '用户名',
    `password` VARCHAR(128) NOT NULL COMMENT '哈希密码',
    `created_at` VARCHAR(36) NOT NULL COMMENT '创建时间',  -- '2025-08-27 15:56:46'

    PRIMARY KEY (id) USING BTREE,
    UNIQUE INDEX uniq_username (username) USING BTREE
) COMMENT='用户表';


CREATE TABLE `post` (
    `id` INT(10) NOT NULL AUTO_INCREMENT,
    `author_id` INT(10) NOT NULL COMMENT 't_user',
    `title` VARCHAR(60) NOT NULL COMMENT '标题',
    `body` TEXT NOT NULL COMMENT '内容',
    `created_at` VARCHAR(36) NOT NULL COMMENT '创建时间',  -- '2025-08-27 15:56:46'

    PRIMARY KEY (id) USING BTREE,
    INDEX idx_author_id (author_id) USING BTREE
) COMMENT='文章表';
