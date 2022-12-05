CREATE TABLE IF NOT EXISTS users (
   id serial PRIMARY KEY,
   username VARCHAR (50) UNIQUE NOT NULL,
   password VARCHAR ( 50 ) NOT NULL,
   email VARCHAR ( 255 ) UNIQUE NOT NULL,
   firstname VARCHAR ( 255 ),
   lastname VARCHAR ( 255 ),
   token VARCHAR(255),
   token_expiration VARCHAR(255)
);