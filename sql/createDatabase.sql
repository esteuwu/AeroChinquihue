-- Airplanes
CREATE TABLE airplanes (airplane TEXT PRIMARY KEY, seats INTEGER);
INSERT INTO airplanes VALUES ('Cessna 208 Caravan', 9);
INSERT INTO airplanes VALUES ('Cessna 310', 5);
INSERT INTO airplanes VALUES ('Let L-410 Turbolet', 19);

-- Destinations
CREATE TABLE destinations (
    destination TEXT PRIMARY KEY, prices TEXT, frequency INTEGER
);
INSERT INTO destinations VALUES ('Ayacara', json_array(30000, 8000), 30);
INSERT INTO destinations VALUES ('Chaitén', json_array(50000, 15000), 45);
INSERT INTO destinations VALUES ('Chepu', json_array(30000, 8000), 60);
INSERT INTO destinations VALUES ('Cochamó', json_array(20000, 5000), 15);
INSERT INTO destinations VALUES ('Contao', json_array(20000, 5000), 120);
INSERT INTO destinations VALUES ('Isla Quenac', json_array(40000, 12000), 180);
INSERT INTO destinations VALUES ('Palqui', json_array(40000, 12000), 45);
INSERT INTO destinations VALUES ('Pillán', json_array(40000, 12000), 45);
INSERT INTO destinations VALUES ('Puelo Bajo', json_array(20000, 5000), 60);
INSERT INTO destinations VALUES ('Pupelde', json_array(25000, 6000), 60);
INSERT INTO destinations VALUES ('Reñihue', json_array(40000, 12000), 30);
INSERT INTO destinations VALUES ('Río Negro', json_array(25000, 6000), 30);
INSERT INTO destinations VALUES (
    'Santa Bárbara', json_array(50000, 15000), 180
);

-- Flights
CREATE TABLE flights (
    uuid TEXT PRIMARY KEY,
    name TEXT,
    identification INTEGER,
    destination TEXT,
    airplane TEXT,
    leave INTEGER,
    seats INTEGER,
    payment_method TEXT,
    cost INTEGER,
    epoch INTEGER
);

-- Freights
CREATE TABLE freights (
    uuid TEXT PRIMARY KEY,
    name TEXT,
    identification INTEGER,
    destination TEXT,
    weight INTEGER,
    payment_method TEXT,
    cost INTEGER,
    epoch INTEGER
);

-- Payment Methods
CREATE TABLE payment_methods (payment_method TEXT PRIMARY KEY);
INSERT INTO payment_methods VALUES ('Efectivo');
INSERT INTO payment_methods VALUES ('Tarjeta de Crédito');
INSERT INTO payment_methods VALUES ('Tarjeta de Débito');
INSERT INTO payment_methods VALUES ('Transferencia');

-- Users
CREATE TABLE users (
    identification INTEGER PRIMARY KEY,
    name TEXT,
    hashed_password TEXT,
    salt TEXT
);
