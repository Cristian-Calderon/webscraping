Hacer tablas:
primero heroes ->

CREATE TABLE heroes (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(255) NOT NULL,
link_img VARCHAR(255) NOT NULL,
link_page VARCHAR(255) NOT NULL
);

Para insertar la base de datos:
iniciar cesion en mysql:
mysql --local-infile=1 -u cris -p

dentro de mysql:
LOAD DATA INFILE '/var/www/webscraping.local/src/scraping/heroes/heroes.csv'
INTO TABLE heroes
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(name, link_img, link_page);

otra tabla:

CREATE TABLE heroes_stats (
id INT AUTO_INCREMENT PRIMARY KEY,
hero_id INT NOT NULL,
popularidad VARCHAR(10),
win_rate VARCHAR(10),
FOREIGN KEY (hero_id) REFERENCES heroes(id)
);


LOAD DATA LOCAL INFILE '/var/www/webscraping.local/src/scraping/perfil/heroes_stats.csv'
INTO TABLE heroes_stats
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(hero_id, popularidad, win_rate);