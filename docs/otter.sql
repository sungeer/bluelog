

CREATE TABLE message (
    id INT AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL COMMENT '用户名',
    body VARCHAR(200) NOT NULL COMMENT '留言',
    is_deleted TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否已删除 0-未删除 1-已删除',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (id)
) COMMENT='留言表';



-- 初始化数据
INSERT INTO message (name, body, create_time) VALUES
('Alice', 'Hello, this is Alice!', '2024-06-01 09:05:00'),
('Bob', 'Just checking in.', '2024-06-01 10:15:00'),
('Charlie', 'How is everyone?', '2024-06-01 11:25:00'),
('David', 'Good morning!', '2024-06-01 12:35:00'),
('Eve', 'Ready for the meeting?', '2024-06-01 13:45:00'),
('Frank', 'Let’s start the project.', '2024-06-01 14:55:00'),
('Grace', 'Can anyone help me?', '2024-06-01 15:05:00'),
('Heidi', 'I will be late today.', '2024-06-01 16:15:00'),
('Ivan', 'Check out this link.', '2024-06-01 17:25:00'),
('Judy', 'Lunch break?', '2024-06-01 18:35:00'),
('Mallory', 'See you all tomorrow.', '2024-06-02 09:05:00'),
('Niaj', 'This is a test message.', '2024-06-02 10:15:00'),
('Olivia', 'Meeting postponed.', '2024-06-02 11:25:00'),
('Peggy', 'Project completed!', '2024-06-02 12:35:00'),
('Quentin', 'Review the documents.', '2024-06-02 13:45:00'),
('Rupert', 'Great job, team!', '2024-06-02 14:55:00'),
('Sybil', 'Who is available now?', '2024-06-02 15:05:00'),
('Trudy', 'Deadline extended.', '2024-06-02 16:15:00'),
('Uma', 'Any questions?', '2024-06-02 17:25:00'),
('Victor', 'Let’s celebrate!', '2024-06-02 18:35:00');

