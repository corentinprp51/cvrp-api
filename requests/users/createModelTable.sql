CREATE TABLE IF NOT EXISTS model (
   id serial PRIMARY KEY,
   user_id SERIAL,
   name VARCHAR (50),
   parameters JSON,
   data_parameters JSON,
   solution JSON,
   solution_path_file VARCHAR (255),
   creation_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
   last_edit TIMESTAMP,
   CONSTRAINT fk_user
   FOREIGN KEY(user_id) 
   REFERENCES users(id)
   ON DELETE CASCADE
);