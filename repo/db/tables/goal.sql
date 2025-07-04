CREATE TABLE `goals` (
    `user_id` VARCHAR(36) NOT NULL,
    `goal_id` VARCHAR(36) PRIMARY KEY NOT NULL,
    `goal_name` VARCHAR(255) NOT NULL,
    `goal_description` VARCHAR(255),
    `goal_target_amount` INT NOT NULL,
    `goal_current_amount` INT NOT NULL DEFAULT 0,
    `is_goal_reached` TINYINT(1) NOT NULL DEFAULT 0,
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
