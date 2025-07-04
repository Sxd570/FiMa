CREATE TABLE `category` (
    `user_id` VARCHAR(36) NOT NULL,
    `category_id` VARCHAR(36) PRIMARY KEY,
    `category_name` VARCHAR(255) NOT NULL,
    `category_description` VARCHAR(255),
    `transaction_type` VARCHAR(36) NOT NULL,
    FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
