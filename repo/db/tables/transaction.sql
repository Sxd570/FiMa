CREATE TABLE `transaction` (
    `user_id` VARCHAR(36) NOT NULL,
    `transaction_id` VARCHAR(36) PRIMARY KEY NOT NULL,
    `category_id` VARCHAR(36) NOT NULL,
    `transaction_type` VARCHAR(36) NOT NULL,
    `transaction_info` VARCHAR(255) NOT NULL,
    `transaction_amount` INT NOT NULL,
    `transaction_date` VARCHAR(50) NOT NULL,
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
    FOREIGN KEY (`category_id`) REFERENCES `budget`(`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
