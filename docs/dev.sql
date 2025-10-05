

CREATE TABLE `org_unit` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `org_code` VARCHAR(32) NOT NULL COMMENT '组织编码，业务稳定标识，弱引用推荐使用；全局唯一',
  `org_name` VARCHAR(128) NOT NULL COMMENT '组织名称，如“XX市教育局”',
  `type_code` VARCHAR(32) NOT NULL COMMENT '组织类型编码，如 EDUCATION/FINANCE 等',
  `parent_code` VARCHAR(32) NULL DEFAULT NULL COMMENT '父组织编码，组织树使用，弱引用到 org_code',
  `level` TINYINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '层级：1-市级，2-区/县级，3-科室/处室等',
  `status` TINYINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态：1-启用，0-停用',
  `contact_phone` VARCHAR(32) NULL DEFAULT NULL COMMENT '对外联系电话（可空）',
  `contact_email` VARCHAR(128) NULL DEFAULT NULL COMMENT '对外邮箱（可空）',
  `remark` VARCHAR(255) NULL DEFAULT NULL COMMENT '备注',
  `created_by` VARCHAR(64) NOT NULL DEFAULT 'system' COMMENT '创建人',
  `updated_by` VARCHAR(64) NOT NULL DEFAULT 'system' COMMENT '更新人',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否删除：0-否，1-是',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_org_code` (`org_code`),
  KEY `idx_type_code` (`type_code`),
  KEY `idx_parent_code` (`parent_code`),
  KEY `idx_level_status` (`level`, `status`),
  CONSTRAINT `chk_org_unit_level` CHECK (`level` IN (1,2,3)),
  CONSTRAINT `chk_org_unit_status` CHECK (`status` IN (0,1))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='组织机构表';


CREATE TABLE `project` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `project_code` VARCHAR(50) NOT NULL COMMENT '项目编码，业务唯一（幂等创建）',
  `project_name` VARCHAR(200) NOT NULL COMMENT '项目名称',
  `org_code` VARCHAR(32) NOT NULL COMMENT '弱引用组织编码（org_unit.org_code）',
  `org_name_snapshot` VARCHAR(128) NOT NULL COMMENT '创建/最后绑定时的组织名称快照，便于历史可读',
  `status` TINYINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态：1-进行中，2-已完成，0-暂停/归档',
  `start_date` DATE NOT NULL COMMENT '开始日期',
  `end_date` DATE NULL DEFAULT NULL COMMENT '结束日期（可空）',
  `budget_amount` DECIMAL(14,2) NULL DEFAULT NULL COMMENT '预算金额，单位元',
  `owner_user_id` BIGINT UNSIGNED NULL DEFAULT NULL COMMENT '负责人用户ID（可弱引用用户中心）',
  `tags` JSON NULL COMMENT '标签JSON数组，如 ["教育信息化","招标"]',
  `remark` VARCHAR(255) NULL DEFAULT NULL COMMENT '备注',
  `created_by` VARCHAR(64) NOT NULL DEFAULT 'system' COMMENT '创建人',
  `updated_by` VARCHAR(64) NOT NULL DEFAULT 'system' COMMENT '更新人',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否删除：0-否，1-是',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_project_code` (`project_code`),
  KEY `idx_org_code` (`org_code`),
  KEY `idx_status_start` (`status`, `start_date`),
  CONSTRAINT `chk_project_status` CHECK (`status` IN (0,1,2)),
  CONSTRAINT `chk_project_date` CHECK (`end_date` IS NULL OR `end_date` >= `start_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='项目表（弱引用组织）';


INSERT INTO org_unit (org_code, org_name, type_code, level, status, created_by, updated_by)
VALUES
 ('CITY_GOV', 'XX市人民政府', 'CITY_GOV', 1, 1, 'init', 'init'),
 ('DEV_REFORM', 'XX市发展和改革委员会', 'DEV_REFORM', 1, 1, 'init', 'init'),
 ('PUBLIC_SECURITY', 'XX市公安局', 'PUBLIC_SECURITY', 1, 1, 'init', 'init'),
 ('EDUCATION', 'XX市教育局', 'EDUCATION', 1, 1, 'init', 'init'),
 ('HEALTH', 'XX市卫生健康委员会', 'HEALTH', 1, 1, 'init', 'init'),
 ('FINANCE', 'XX市财政局', 'FINANCE', 1, 1, 'init', 'init');

INSERT INTO project (project_code, project_name, org_code, org_name_snapshot, status, start_date, budget_amount, created_by, updated_by)
VALUES
 ('PRJ-2025-001', '智慧校园平台', 'EDUCATION', 'XX市教育局', 1, '2025-01-15', 12000000.00, 'init', 'init'),
 ('PRJ-2025-002', '市级医保结算优化', 'HEALTH', 'XX市卫生健康委员会', 1, '2025-02-01', 8000000.00, 'init', 'init');

