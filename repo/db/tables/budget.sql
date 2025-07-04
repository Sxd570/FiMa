CREATE TABLE `budget` (
    `user_id` VARCHAR(36) NOT NULL,
    `category_id` VARCHAR(36) NOT NULL,
    `budget_id` VARCHAR(36) PRIMARY KEY NOT NULL,
    `budget_allocated_amount` INT NOT NULL,
    `budget_spent_amount` INT NOT NULL,
    `budget_allocated_month` VARCHAR(7) NOT NULL,
    `is_budget_limit_reached` TINYINT(1) NOT NULL DEFAULT 0,
    `is_budget_over_limit` TINYINT(1) NOT NULL DEFAULT 0,
    FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
    FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;