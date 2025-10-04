-- 库级别建议：
-- CREATE DATABASE IF NOT EXISTS `shop`
--   DEFAULT CHARACTER SET utf8mb4
--   COLLATE utf8mb4_0900_ai_ci;


-- 1) 商品表
DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `id`            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增主键ID',
  `sku`           VARCHAR(64)     NOT NULL COMMENT '商品SKU，业务唯一',
  `product_name`  VARCHAR(128)    NOT NULL COMMENT '商品名称',
  `category_id`   BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '类目ID（弱关联）',
  `seller_id`     BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '商家ID（弱关联）',
  `price_cent`    INT UNSIGNED    NOT NULL COMMENT '价格(分)',
  `stock`         INT UNSIGNED    NOT NULL DEFAULT 0 COMMENT '库存数量',
  `status`        TINYINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态：1-上架 2-下架 3-禁售',
  `version`       INT UNSIGNED    NOT NULL DEFAULT 1 COMMENT '乐观锁版本号',
  `is_deleted`    TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否删除：0-否 1-是',
  `creator`       VARCHAR(64)     NOT NULL DEFAULT '' COMMENT '创建人',
  `updater`       VARCHAR(64)     NOT NULL DEFAULT '' COMMENT '更新人',
  `create_time`   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time`   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_sku` (`sku`),
  -- 按业务需要可做前缀索引以降低索引大小，示例采用前缀 64（与列等长，亦可酌情缩短）
  KEY `idx_product_name` (`product_name`),
  KEY `idx_seller_status` (`seller_id`, `status`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci
  ROW_FORMAT=DYNAMIC
  COMMENT='商品表';


-- 2) 订单主表
DROP TABLE IF EXISTS `order_main`;
CREATE TABLE `order_main` (
  `id`            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增主键ID',
  `order_no`      VARCHAR(64)     NOT NULL COMMENT '订单号，业务唯一',
  `buyer_id`      BIGINT UNSIGNED NOT NULL COMMENT '买家ID（弱关联）',
  `seller_id`     BIGINT UNSIGNED NOT NULL COMMENT '商家ID（弱关联）',
  `total_amount_cent` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '订单总金额(分)',
  `pay_amount_cent`   INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '实付金额(分)',
  `order_status`  TINYINT UNSIGNED NOT NULL DEFAULT 10 COMMENT '订单状态：10-待支付 20-已支付 30-已发货 40-已完成 50-已关闭',
  `pay_time`      DATETIME        NULL DEFAULT NULL COMMENT '支付时间',
  `version`       INT UNSIGNED    NOT NULL DEFAULT 1 COMMENT '乐观锁版本号',
  `is_deleted`    TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否删除：0-否 1-是',
  `creator`       VARCHAR(64)     NOT NULL DEFAULT '' COMMENT '创建人',
  `updater`       VARCHAR(64)     NOT NULL DEFAULT '' COMMENT '更新人',
  `create_time`   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time`   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  KEY `idx_buyer` (`buyer_id`),
  KEY `idx_seller` (`seller_id`),
  KEY `idx_status_ctime` (`order_status`, `create_time`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci
  ROW_FORMAT=DYNAMIC
  COMMENT='订单主表';


-- 3) 订单明细表（不建外键，使用弱关联字段）
DROP TABLE IF EXISTS `order_item`;
CREATE TABLE `order_item` (
  `id`            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增主键ID',
  `order_id`      BIGINT UNSIGNED NOT NULL COMMENT '订单主表ID（弱关联 order_main.id）',
  `product_id`    BIGINT UNSIGNED NOT NULL COMMENT '商品ID（弱关联 product.id）',
  `seller_id`     BIGINT UNSIGNED NOT NULL COMMENT '商家ID（冗余方便查询）',
  `sku`           VARCHAR(64)     NOT NULL COMMENT '冗余SKU，便于对账',
  `product_name`  VARCHAR(128)    NOT NULL DEFAULT '' COMMENT '下单时商品名快照',
  `price_cent`    INT UNSIGNED    NOT NULL COMMENT '下单单价(分)',
  `quantity`      INT UNSIGNED    NOT NULL COMMENT '购买数量',
  `amount_cent`   INT UNSIGNED    NOT NULL COMMENT '小计金额(分)=price_cent*quantity',
  `version`       INT UNSIGNED    NOT NULL DEFAULT 1 COMMENT '乐观锁版本号',
  `is_deleted`    TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否删除：0-否 1-是',
  `creator`       VARCHAR(64)     NOT NULL DEFAULT '' COMMENT '创建人',
  `updater`       VARCHAR(64)     NOT NULL DEFAULT '' COMMENT '更新人',
  `create_time`   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time`   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  -- 组合唯一：一个订单里同一商品只出现一行
  UNIQUE KEY `uk_order_product` (`order_id`, `product_id`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_seller_id` (`seller_id`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci
  ROW_FORMAT=DYNAMIC
  COMMENT='订单明细表';