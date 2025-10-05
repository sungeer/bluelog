-- 建议库级设置：
-- CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci
-- sql_mode 含 STRICT_ALL_TABLES
-- 时区统一为 +00:00（应用层做时区转换）

/* 1) 用户表：支持登录验证 */
CREATE TABLE users (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'PK',
  biz_id          CHAR(26) NOT NULL COMMENT '业务幂等ID，建议ULID',
  username        VARCHAR(64) NOT NULL COMMENT '登录名，唯一',
  email           VARCHAR(128) NOT NULL COMMENT '邮箱，唯一',
  password_hash   VARCHAR(255) NOT NULL COMMENT '密码哈希，建议BCrypt/Argon2',
  password_salt   VARCHAR(64) NULL COMMENT '若算法需要',
  status          VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT 'active/locked/disabled',
  last_login_at   DATETIME(3) NULL COMMENT '最近登录时间',
  display_name    VARCHAR(128) NOT NULL COMMENT '显示名/昵称',
  remarks         VARCHAR(512) NULL COMMENT '备注',
  created_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  updated_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  created_by      BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '创建人ID（系统为0）',
  updated_by      BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '更新人ID（系统为0）',
  deleted         TINYINT(1) NOT NULL DEFAULT 0 COMMENT '软删除标记',
  PRIMARY KEY (`id`),
  UNIQUE KEY uk_users_biz_id (biz_id),
  UNIQUE KEY uk_users_username (username),
  UNIQUE KEY uk_users_email (email),
  KEY idx_users_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户';


/* 2) 公司软件清单：记录公司有哪些软件（可选归属组织、负责人） */
CREATE TABLE softwares (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'PK',
  biz_id          CHAR(26) NOT NULL COMMENT '业务幂等ID',
  software_key    VARCHAR(64) NOT NULL COMMENT '软件唯一码，便于人读与集成，唯一',
  software_name   VARCHAR(128) NOT NULL COMMENT '软件名称',
  remarks         VARCHAR(512) NULL COMMENT '备注',
  status          VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT 'active/inactive/archived',
  created_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  updated_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  created_by      BIGINT UNSIGNED NOT NULL DEFAULT 0,
  updated_by      BIGINT UNSIGNED NOT NULL DEFAULT 0,
  deleted         TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY uk_softwares_biz_id (biz_id),
  UNIQUE KEY uk_softwares_key (software_key),
  KEY idx_softwares_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='公司软件清单';


-- Users
INSERT INTO users
(biz_id, username, email, password_hash, password_salt, status, last_login_at, display_name, remarks, created_at, updated_at, created_by, updated_by, deleted)
VALUES
('01JAK0VQ2Y9G6WQ6QH2J0C3P4Z', 'admin',   'admin@example.com', '$2y$12$0JqkDqQeS2mXn7H3zU8mG.f7WwJd1mP6Wf7Y7Qw0c8mNQn1h3mC5i', NULL, 'active',   '2025-10-01 09:15:23.123', '系统管理员', '超管账户',          NOW(3), NOW(3), 0, 0, 0),
('01JAK0VQ2Y9G6WQ6QH2J0C3P51', 'alice',   'alice@example.com', '$2y$12$0JqkDqQeS2mXn7H3zU8mG.f7WwJd1mP6Wf7Y7Qw0c8mNQn1h3mC5i', NULL, 'active',   '2025-10-02 12:01:00.000', 'Alice Chen',  '研发部后端',        NOW(3), NOW(3), 0, 0, 0),
('01JAK0VQ2Y9G6WQ6QH2J0C3P52', 'bob',     'bob@example.com',   '$2y$12$0JqkDqQeS2mXn7H3zU8mG.f7WwJd1mP6Wf7Y7Qw0c8mNQn1h3mC5i', NULL, 'locked',   '2025-09-27 18:33:45.550', 'Bob Li',      '三次失败已锁定',    NOW(3), NOW(3), 0, 0, 0),
('01JAK0VQ2Y9G6WQ6QH2J0C3P53', 'carol',   'carol@example.com', '$2y$12$0JqkDqQeS2mXn7H3zU8mG.f7WwJd1mP6Wf7Y7Qw0c8mNQn1h3mC5i', NULL, 'disabled', NULL,                    'Carol Wang',  '离职已禁用',        NOW(3), NOW(3), 0, 0, 0),
('01JAK0VQ2Y9G6WQ6QH2J0C3P54', 'david',   'david@example.com', '$2y$12$0JqkDqQeS2mXn7H3zU8mG.f7WwJd1mP6Wf7Y7Qw0c8mNQn1h3mC5i', NULL, 'active',   NULL,                    'David Zhao',  '试用账号，月底删除', NOW(3), NOW(3), 0, 0, 0);

-- Company Softwares
INSERT INTO softwares
(biz_id, software_key, software_name, remarks, status, created_at, updated_at, created_by, updated_by, deleted)
VALUES
('01JAK0W0Z8QK4P4F1X2K8S8R01', 'erp',            '集团ERP系统',               '核心财务/采购/库存',                    'active',   NOW(3), NOW(3), 0, 0, 0),
('01JAK0W0Z8QK4P4F1X2K8S8R02', 'crm',            '客户关系管理',               '销售线索、合同、回款',                  'active',   NOW(3), NOW(3), 0, 0, 0),
('01JAK0W0Z8QK4P4F1X2K8S8R03', 'intranet',       '内部门户',                   'OA/公告/流程',                          'active',   NOW(3), NOW(3), 0, 0, 0),
('01JAK0W0Z8QK4P4F1X2K8S8R04', 'data-platform',  '数据中台',                   'ETL/指标/报表，负责人Alice',           'active',   NOW(3), NOW(3), 0, 0, 0),
('01JAK0W0Z8QK4P4F1X2K8S8R05', 'legacy-hr',      '人力系统（旧）',             '计划2026Q1下线',                       'inactive', NOW(3), NOW(3), 0, 0, 0),
('01JAK0W0Z8QK4P4F1X2K8S8R06', 'mobile-app',     '公司移动应用',               'iOS/Android 客户端，负责人David',      'active',   NOW(3), NOW(3), 0, 0, 0);

-- 常用查询样例
-- 1) 登录校验获取密码哈希
-- SELECT id, password_hash, status FROM users WHERE username = ? AND deleted = 0 LIMIT 1;

-- 2) 列出在用软件
-- SELECT software_key, software_name, remarks FROM softwares WHERE status='active' AND deleted=0 ORDER BY software_key;
