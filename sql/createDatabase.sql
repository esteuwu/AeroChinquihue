-- Airplanes
CREATE TABLE airplanes(airplane);
INSERT INTO airplanes VALUES('Cessna 208 Caravan');
INSERT INTO airplanes VALUES('Cessna 310');
INSERT INTO airplanes VALUES('Let L-410 Turbolet');
-- Flights
CREATE TABLE flights(destination, prices, frequency);
INSERT INTO flights VALUES ('Ayacara', json_array(30000, 8000), 30);
INSERT INTO flights VALUES ('Chaitén', json_array(50000, 15000), 45);
INSERT INTO flights VALUES ('Chepu', json_array(30000, 8000), 60);
INSERT INTO flights VALUES ('Cochamó', json_array(20000, 5000), 15);
INSERT INTO flights VALUES ('Contao', json_array(20000, 5000), 120);
INSERT INTO flights VALUES ('Isla Quenac', json_array(40000, 12000), 180);
INSERT INTO flights VALUES ('Palqui', json_array(40000, 12000), 45);
INSERT INTO flights VALUES ('Pillán', json_array(40000, 12000), 45);
INSERT INTO flights VALUES ('Puelo Bajo', json_array(20000, 5000), 60);
INSERT INTO flights VALUES ('Pupelde', json_array(25000, 6000), 60);
INSERT INTO flights VALUES ('Reñihue', json_array(40000, 12000), 30);
INSERT INTO flights VALUES ('Río Negro', json_array(25000, 6000), 30);
INSERT INTO flights VALUES ('Santa Bárbara', json_array(50000, 15000), 180);
-- Payment Methods
CREATE TABLE paymentMethods(paymentMethod);
INSERT INTO paymentMethods VALUES('Efectivo');
INSERT INTO paymentMethods VALUES('Tarjeta de Crédito');
INSERT INTO paymentMethods VALUES('Tarjeta de Débito');
INSERT INTO paymentMethods VALUES('Transferencia');
