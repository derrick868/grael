PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE customer (
	id INTEGER NOT NULL, 
	email VARCHAR(100), 
	status VARCHAR(100), 
	username VARCHAR(100), 
	password_hash VARCHAR(150), 
	date_joined DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
INSERT INTO customer VALUES(1,'derrickndirangu868@gmail.com','admin','derro','scrypt:32768:8:1$pIDFUyd21MihegOj$76022c66f5fc4aed41b9bf6fde9eddd0d430e3e3b53f0cee81396acdfabbc295bfed934809d752d01a74bc2c3715cc48bab9841b3fca11566f5cd4a18d4be9e0','2025-04-09 12:42:02.200496');
INSERT INTO customer VALUES(2,'derrickmacha1@gmail.com','admin','derro','scrypt:32768:8:1$jvJ7C6feanAd1hPH$8bfcfbeeef2b2ffc07e8f98dc19d8813cdb0004c054b897cacbbb5a9687e88e5320b7192edbc5d35f8954aeecd32a4eb0cdb6c4197072898aa62610476949e2f','2025-04-11 10:32:56.004526');
CREATE TABLE product (
	id INTEGER NOT NULL, 
	product_name VARCHAR(100) NOT NULL, 
	current_price FLOAT NOT NULL, 
	previous_price FLOAT NOT NULL, 
	in_stock INTEGER NOT NULL, 
	product_picture VARCHAR(1000) NOT NULL, 
	flash_sale BOOLEAN, 
	date_added DATETIME, 
	PRIMARY KEY (id)
);
INSERT INTO product VALUES(2,'jug2',34.0,45.0,-1,'./media/Screenshot_20250406_080212_1.jpg',0,'2025-04-09 14:52:15.588460');
INSERT INTO product VALUES(3,'jug3',39.0,48.0,3,'./media/WhatsApp_Image_2025-04-05_at_15.59.18.jpeg',0,'2025-04-09 14:53:17.524638');
INSERT INTO product VALUES(4,'jug5',38.0,49.0,87,'./media/WhatsApp_Image_2025-04-05_at_15.59.11.jpeg',0,'2025-04-09 14:53:41.111096');
INSERT INTO product VALUES(5,'cup',200.0,300.0,30,'./media/Screenshot_20250406_080212_1.jpg',1,'2025-04-10 17:10:36.114538');
CREATE TABLE cart (
	id INTEGER NOT NULL, 
	quantity INTEGER NOT NULL, 
	customer_link INTEGER NOT NULL, 
	product_link INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(customer_link) REFERENCES customer (id), 
	FOREIGN KEY(product_link) REFERENCES product (id)
);
CREATE TABLE IF NOT EXISTS "order" (
	id INTEGER NOT NULL, 
	quantity INTEGER NOT NULL, 
	price FLOAT NOT NULL, 
	status VARCHAR(100) NOT NULL, 
	payment_id VARCHAR(1000) NOT NULL, 
	customer_link INTEGER NOT NULL, 
	product_link INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(customer_link) REFERENCES customer (id), 
	FOREIGN KEY(product_link) REFERENCES product (id)
);
INSERT INTO "order" VALUES(1,1,34.0,'Accepted','1',1,2);
INSERT INTO "order" VALUES(2,3,39.0,'Delivered','3',1,3);
COMMIT;
