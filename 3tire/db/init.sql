CREATE DATABASE IF NOT EXISTS coderdb;
USE coderdb;

CREATE TABLE IF NOT EXISTS messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  text VARCHAR(255) NOT NULL
);

INSERT IGNORE INTO messages (id, text) VALUES
(1, 'Hello from the three-tier coder app!');
