
CREATE TABLE users
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


CREATE TABLE brands
(   
    id SERIAL PRIMARY KEY NOT NULL,
    uuid UUID DEFAULT gen_random_uuid() NOT NULL,
    brand_name VARCHAR(300) UNIQUE NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

INSERT INTO brands (brand_name) VALUES 
('Toyota'),
('Ford'),
('Chevrolet'),
('Volkswagen'),
('Nissan'),
('Hyundai'),
('Kia'),
('Subaru'),
('Mazda'),
('Renault'),
('Dodge');


CREATE TABLE vehicles
(   
    id SERIAL PRIMARY KEY NOT NULL,
    uuid UUID DEFAULT gen_random_uuid() NOT NULL,
    brand_id INTEGER NOT NULL,
    complement VARCHAR(10000),
    year INT NOT NULL CHECK (year >= 1886 AND year <= EXTRACT(YEAR FROM CURRENT_DATE)),
    color VARCHAR(200),
    plate VARCHAR(50) UNIQUE NOT NULL,
    price BIGINT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE NOT NULL,

    CONSTRAINT fk_brand FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE RESTRICT
);

INSERT INTO vehicles (brand_id, complement, year, color, price, plate) values
(1, 'Corolla XEi 2.0 Flex 16V Aut. 2020', 2020, 'Prata', 15000000, 'ABC1234'),
(2, 'F-150 Lariat 3.5 V6 EcoBoost 4x4 Aut. 2021', 2021, 'Preta', 30000000, 'XYZ5678'),
(3, 'Silverado LTZ 5.3 V8 FlexPower Aut. 2018', 2018, 'Branca', 25000000, 'DEF9876'),
(4, 'Golf GTI 2.0 TSI DSG 2023', 2023, 'Vermelha', 20000000, 'GHI4567'),
(5, 'Sentra SL 2.0 CVT 2023', 2023, 'Azul', 12000000, 'JKL3456'),
(6, 'Elantra Limited 2.0 Flex Aut. 2023', 2023, 'Cinza', 13000000, 'MNO7890'),
(7, 'Sportage EX2 V6 Flex Aut. 2022', 2022, 'Preta', 14000000, 'PQR1234'),
(8, 'Outback AWD GT Híbrido Flex Aut. 2023', 2023, 'Prata', 18000000, 'STU5678'),
(9, 'CX-5 Grand Touring AWD Híbrido Flex Aut. 2019', 2019, 'Branca', 16000000, 'VWX9876'),
(10, 'Duster Iconic 1.6 Flex Aut. 2017', 2017, 'Amarela', 11000000, 'YZA4321'),
(11, 'Durango Citadel Híbrida Flex Aut. 2024', 2024, 'Vermelha', 22000000, 'BCD7654');