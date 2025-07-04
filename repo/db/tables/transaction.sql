-- Transaction Table
CREATE TABLE `transaction` (
    `transaction_id` VARCHAR(36) PRIMARY NOT NULL,
    `user_id` VARCHAR(36) NOT NULL,
    `category_id` VARCHAR(36) NOT NULL,
    `transaction_type_id` VARCHAR(36) NOT NULL,
    `transaction_info` VARCHAR(255) NOT NULL,
    `transaction_amount` INT NOT NULL,
    `transaction_date` VARCHAR(50) NOT NULL,
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
    FOREIGN KEY (`category_id`) REFERENCES `category`(`category_id`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
