---
--- Drop tables
---

DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS Storage;
DROP TABLE IF EXISTS Birthday;
DROP TABLE IF EXISTS Pokemon;
DROP TABLE IF EXISTS PokeDex;
DROP TABLE IF EXISTS Client;

---
--- Create tables
---

CREATE TABLE PokeDex (
    dex_num int not null,
    dex_name text,
    type text,
    weight float,
    height float,
    PRIMARY KEY (dex_num)
);

CREATE TABLE Client (
    owner_id int not null,
    name text,
    address text,
    phone_num text,
    PRIMARY KEY (owner_id)
);

CREATE TABLE Pokemon (
    poke_id int not null,
    owner_id int references Client(owner_id),
    pokedex_num int references PokeDex(dex_num),
    name text,
    level int not null check (level between 1 and 100),
    gender text not null,
    PRIMARY KEY (poke_id)
);

CREATE TABLE Birthday (
    child int unique references Pokemon(poke_id),
    parent_m int references Pokemon(poke_id),
    parent_f int references Pokemon(poke_id),
    birthday date,
    PRIMARY KEY (child, parent_m, parent_f)
);

CREATE TABLE Storage (
    room_num text not null,
    PRIMARY KEY (room_num)
);

CREATE TABLE Booking (
  booking_id int not null,
  room_num text references Storage(room_num),
  poke_id int references Pokemon(poke_id),
  date_in date,
  date_out date,
  PRIMARY KEY (booking_id)
);

---
--- Insert values
---

INSERT INTO Client
VALUES (100001, 'John Freeman', '1234 Dummy Street', '812-905-0111');

INSERT INTO Client
VALUES (100002, 'George Gore', '8585 Blessings Lane', '502-857-3847');

INSERT INTO Client
VALUES (100003, 'Jane McLane', '9345 Blaze Street', '382-394-2937');

INSERT INTO Client
VALUES (100004, 'Bob Jobs', '4201 9th Ave', '390-392-2929');

INSERT INTO Client
VALUES (100005, 'Victor Smith', '3890 10th Ave', '809-405-4930');

--PokeDex Table Inserts
INSERT INTO PokeDex
VALUES (1, 'Bulbasuar', 'Grass/Poison', 15.2, 28);

INSERT INTO PokeDex
VALUES (4, 'Charmander', 'Fire', 18.7, 24);

INSERT INTO PokeDex
VALUES (7, 'Squirtle', 'Water', 19.8, 20);

INSERT INTO PokeDex
VALUES (25, 'Pikachu', 'Electric', 13.2, 16);

INSERT INTO PokeDex
VALUES (039, 'Jigglypuff', 'Normal-Fairy', 12.1, 20);

INSERT INTO PokeDex
VALUES (078, 'Rapidash', 'Fire', 209.4, 67);

INSERT INTO PokeDex
VALUES (120, 'Staryu', 'Water', 76.1, 31);

INSERT INTO PokeDex
VALUES (133, 'Eevee', 'Normal', 14.3, 12);

INSERT INTO PokeDex
VALUES (132, 'Ditto', 'Normal', 8.8, 12);

--Storage Table Inserts
INSERT INTO Storage
VALUES ('101');

INSERT INTO Storage
VALUES ('102');

INSERT INTO Storage
VALUES ('103');

INSERT INTO Storage
VALUES ('104');

INSERT INTO Storage
VALUES ('A1');

INSERT INTO Storage
VALUES ('A2');

INSERT INTO Storage
VALUES ('A3');

--Pokemon Table Inserts
INSERT INTO Pokemon
VALUES (23489, 100001, 1, 'Bulby', 20, 'Male');

INSERT INTO Pokemon
VALUES (23765, 100001, 4, 'Charmander', 5, 'Female');

INSERT INTO Pokemon
VALUES (48376, 100001, 132, 'Ditto', 9, 'Male');

INSERT INTO Pokemon
VALUES (01928, 100001, 7, 'Squirty', 35, 'Female');

INSERT INTO Pokemon
VALUES (61726, 100001, 7, 'Squirtle', 1, 'Male');

INSERT INTO Pokemon
VALUES (23498, 100001, 132, 'Diiito', 3, 'Female');

--Birthday Table Inserts
INSERT INTO Birthday
VALUES (61726, 48376, 01928, '4-21-2023');

INSERT INTO birthday
VALUES (23498, 48376, 01928, '4-15-2023');

--Booking Table Inserts
INSERT INTO Booking
VALUES (12387, '101', 23489, '4-20-2023', '4-21-2023');

INSERT INTO Booking
VALUES (12863, '102', 23765, '4-20-2023', NULL);

INSERT INTO Booking
VALUES (94876, '103', 48376, '4-20-2023', NULL);

INSERT INTO Booking
VALUES (90282, '104', 01928, '4-20-2023', NULL);

INSERT INTO Booking
VALUES (74365, 'A1', 61726, '4-22-2023', NULL);

INSERT INTO Booking
VALUES (35292, 'A2', 23498, '4-24-2023', NULL);