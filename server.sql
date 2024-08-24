CREATE TABLE users (
  username VARCHAR(18) NOT NULL,
  password VARCHAR(255),
  rating INTEGER DEFAULT 1200,
  PRIMARY KEY (username)
);
