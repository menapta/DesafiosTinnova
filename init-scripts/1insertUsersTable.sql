
CREATE TABLE IF NOT EXISTS users
(   
    id SERIAL PRIMARY KEY NOT NULL,
    uuid UUID DEFAULT gen_random_uuid() NOT NULL,
    username VARCHAR(300) UNIQUE NOT NULL,
    passwordcrypt TEXT NOT NULL,
    usertype VARCHAR(50) NOT NULL,
    datecreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

INSERT INTO users (username, passwordcrypt, usertype) VALUES ('admin', '$2b$12$mBHZZAiUYZak2F5.RHI11OF2L2IeT9ytx7Y73Q18O1gtHoulxP7Bi', 'admin');
INSERT INTO users (username, passwordcrypt, usertype) VALUES ('teobaldo', '$2b$12$mBHZZAiUYZak2F5.RHI11OF2L2IeT9ytx7Y73Q18O1gtHoulxP7Bi', 'user');

