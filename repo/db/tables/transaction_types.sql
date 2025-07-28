CREATE TABLE `transaction_type` (
    `user_id` VARCHAR(36) NOT NULL,
    `transaction_type_id` VARCHAR(36) PRIMARY KEY NOT NULL,
    `transaction_type_name` VARCHAR(255) NOT NULL,
    `transaction_type_description` VARCHAR(255),
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
