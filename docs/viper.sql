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


-- 清空旧数据
-- TRUNCATE TABLE blessing;
-- TRUNCATE TABLE user_account;

-- 插入一个示例用户
INSERT INTO user_account (
  username, display_name, password_hash, password_salt, status
) VALUES
  ('alice', 'Alice', '$argon2id$v=19$m=65536,t=3,p=1$sampleSalt$sampleHash', 'sampleSalt', 1);

-- 获取该用户的ID（MySQL会话内）
SET @uid := LAST_INSERT_ID();

-- 为该用户插入多条祝福语
INSERT INTO blessing (user_id, text, status) VALUES
  (@uid, '今天的你，配得上所有认真带来的好运。', 1),
  (@uid, '把难题切小，一口一口吃掉，它就不再可怕。', 1),
  (@uid, '哪怕只前进一步，也是在超越昨天的自己。', 1),
  (@uid, '专注当下这一件事，你会比想象中更快抵达。', 1),
  (@uid, '温柔待己，坚定向前，光会沿路照进来。', 1),
  (@uid, '给自己一个开始，剩下的交给坚持。', 1),
  (@uid, '把计划写小一点，把行动做实一点。', 1),
  (@uid, '困难不是路墙，是路标。', 1),
  (@uid, '情绪来了先呼吸三次，再做决定。', 1),
  (@uid, '比起完美，完成更重要。', 1),
  (@uid, '把今天过好，明天自然会来。', 1),
  (@uid, '向前的每一步，都算数。', 1),
  (@uid, '请相信，长期主义会给你惊喜。', 1),
  (@uid, '把注意力从“结果”挪到“下一步”。', 1),
  (@uid, '自律不是束缚，是给梦想让路。', 1),
  (@uid, '把手机放下十分钟，你会找回主动权。', 1),
  (@uid, '你努力的样子，正在被未来默默记录。', 1),
  (@uid, '别和昨天的失败纠缠，和今天的行动拥抱。', 1),
  (@uid, '把目标拆成今天能做到的一小步。', 1),
  (@uid, '请对自己温柔，也对目标坚定。', 1),
  (@uid, '光会来，但你要先走。', 1),
  (@uid, '愿你在忙碌里，也能记得喝水和微笑。', 1),
  (@uid, '把注意力留给重要的事，把情绪交给时间。', 1),
  (@uid, '每一次尝试，都在增加好运的概率。', 1),
  (@uid, '先把桌面清理干净，大脑也会清爽。', 1),
  (@uid, '慢一点没关系，但请一直在路上。', 1),
  (@uid, '做对的小事，重复做，就是大事。', 1),
  (@uid, '你的坚持，正在悄悄铸造独一无二。', 1),
  (@uid, '把焦虑写下来，然后从第一件开始做。', 1),
  (@uid, '请相信，当下的认真，都是未来的铺垫。', 1);

-- 可选：再插入一个处于禁用状态的祝福语，便于测试过滤
INSERT INTO blessing (user_id, text, status)
VALUES (@uid, '这条被禁用，用于测试列表过滤。', 0);

-- 查询校验
-- 1) 看看用户ID
SELECT id, username, display_name FROM user_account WHERE username = 'alice';

-- 2) 该用户的启用祝福语（最近插入的在后）
SELECT id, user_id, text, status, created_at
FROM blessing
WHERE user_id = @uid AND status = 1 AND is_deleted = 0
ORDER BY id ASC
LIMIT 100;

-- 3) 统计该用户启用/禁用数量
SELECT status, COUNT(*) AS cnt
FROM blessing
WHERE user_id = @uid AND is_deleted = 0
GROUP BY status;

-- 4) 随机取一条（演示用途）
SELECT id, text
FROM blessing
WHERE user_id = @uid AND status = 1 AND is_deleted = 0
ORDER BY RAND()
LIMIT 1;




