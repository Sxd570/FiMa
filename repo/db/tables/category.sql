CREATE TABLE `category` (
    `user_id` VARCHAR(36) NOT NULL,
    `transaction_type_id` VARCHAR(36) NOT NULL,
    `category_id` VARCHAR(36) PRIMARY KEY,
    `category_name` VARCHAR(255) NOT NULL,
    `category_description` VARCHAR(255),
    FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
    FOREIGN KEY (`transaction_type_id`) REFERENCES `transaction_types` (`transaction_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
