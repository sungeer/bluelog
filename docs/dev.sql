

CREATE TABLE `message` (
    `id` INT AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL COMMENT '用户名',
    `body` VARCHAR(200) NOT NULL COMMENT '留言',
    `is_deleted` TINYINT(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否已删除 0-未删除 1-已删除',
    `created_at` VARCHAR(20) NOT NULL COMMENT '创建时间',  -- '2025-08-27 15:56:46'

    PRIMARY KEY (id)
) COMMENT='留言表';


-- 初始化数据
INSERT INTO message (name, body, create_time) VALUES
('Alice', 'Hello, this is Alice!', '2025-09-01 09:05:00'),
('Bob', 'Just checking in.', '2025-09-01 10:15:00'),
('Charlie', 'How is everyone?', '2025-09-02 11:25:00'),
('David', 'Good morning!', '2025-09-03 12:35:00'),
('Eve', 'Ready for the meeting?', '2025-09-05 13:45:00'),
('Frank', 'Let’s start the project.', '2025-09-05 14:55:00'),
('Grace', 'Can anyone help me?', '2025-09-08 15:05:00'),
('Heidi', 'I will be late today.', '2025-09-08 16:15:00'),
('Ivan', 'Check out this link.', '2025-09-08 17:25:00'),
('Judy', 'Lunch break?', '2025-09-08 18:35:00'),
('Mallory', 'See you all tomorrow.', '2025-09-13 09:05:00'),
('Niaj', 'This is a test message.', '2025-09-13 10:15:00'),
('Olivia', 'Meeting postponed.', '2025-09-02 11:25:00'),
('Peggy', 'Project completed!', '2025-09-13 12:35:00'),
('Quentin', 'Review the documents.', '2025-09-02 13:45:00'),
('Rupert', 'Great job, team!', '2025-09-21 14:55:00'),
('Sybil', 'Who is available now?', '2025-09-21 15:05:00'),
('Trudy', 'Deadline extended.', '2025-09-21 16:15:00'),
('Uma', 'Any questions?', '2025-09-21 17:25:00'),
('Victor', 'Let’s celebrate!', '2025-09-21 18:35:00');





