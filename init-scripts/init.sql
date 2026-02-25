CREATE TABLE identity
(
    _name VARCHAR(255),
    surname VARCHAR(255)
);


CREATE TABLE users
(   
    id SERIAL PRIMARY KEY NOT NULL,
    uuid UUID DEFAULT gen_random_uuid(),
    username VARCHAR(255),
    passwordcrypt TEXT,
    typeuser VARCHAR(50)
);

INSERT INTO users (username, passwordcrypt, typeuser) VALUES ('admin', '$2b$12$mBHZZAiUYZak2F5.RHI11OF2L2IeT9ytx7Y73Q18O1gtHoulxP7Bi', 'admin');
INSERT INTO users (username, passwordcrypt, typeuser) VALUES ('teobaldo', '$2b$12$mBHZZAiUYZak2F5.RHI11OF2L2IeT9ytx7Y73Q18O1gtHoulxP7Bi', 'user');