-- Creacion de tabla heroes
drop table if exists heroes;
CREATE TABLE heroes (
    id_heroe INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL,
    link_img TEXT,
    link_page TEXT
);

-- Para cargar los datos de tabla heroes.csv:
--portatil
LOAD DATA INFILE '/var/lib/mysql-files/heroes-spanish.csv'
INTO TABLE heroes
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(nombre, link_img, link_page);

LOAD DATA INFILE '/var/www/webscraping.local/src/scraping/heroes/heroes-spanish.csv'
INTO TABLE heroes
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(nombre, link_img, link_page);



-- Creacion de tabla perfil_heroes
drop table if exists perfil_heroes;
CREATE TABLE perfil_heroes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_heroe INT,
    popularidad VARCHAR(50),
    porcentaje_victoria VARCHAR(50),
    resultado ENUM('won', 'lost'),
    fuerza VARCHAR(50),
    agilidad VARCHAR(50),
    inteligencia VARCHAR(50),
    velocidad_movimiento VARCHAR(50),
    rango_vision VARCHAR(50),
    armadura VARCHAR(50),
    tiempo_ataque_base VARCHAR(50),
    damage VARCHAR(50),
    punto_ataque VARCHAR(50),
    FOREIGN KEY (id_heroe) REFERENCES heroes(id_heroe) ON DELETE CASCADE
);

--portatil
LOAD DATA INFILE '/var/lib/mysql-files/dota_heroes_data.csv'
INTO TABLE perfil_heroes
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@heroe, popularidad, porcentaje_victoria, resultado, fuerza, agilidad, inteligencia, velocidad_movimiento, rango_vision, armadura, tiempo_ataque_base, damage, punto_ataque)
SET id_heroe = (SELECT id_heroe FROM heroes WHERE nombre = @heroe);

-- Para cargar los datos de tabla perfil_heroes.csv
LOAD DATA INFILE '/var/www/webscraping.local/src/scraping/perfil-mejorado/dota_heroes_data.csv'
INTO TABLE perfil_heroes
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@heroe, popularidad, porcentaje_victoria, resultado, fuerza, agilidad, inteligencia, velocidad_movimiento, rango_vision, armadura, tiempo_ataque_base, damage, punto_ataque)
SET id_heroe = (SELECT id_heroe FROM heroes WHERE nombre = @heroe);


-- Creacion de tabla habilidades
drop table if exists habilidades;
CREATE TABLE habilidades (
    id_habilidad INT AUTO_INCREMENT PRIMARY KEY,
    id_heroe INT,
    nombre_habilidad VARCHAR(255),
    descripcion TEXT,
    imagen TEXT,
    FOREIGN KEY (id_heroe) REFERENCES heroes(id_heroe) ON DELETE CASCADE
);

--portatil
LOAD DATA INFILE '/var/lib/mysql-files/dota_heroes_abilities_o.csv'
INTO TABLE habilidades
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@id_habilidad, @id_heroe, @heroe, nombre_habilidad, descripcion, imagen)
SET id_heroe = (SELECT id_heroe FROM heroes WHERE nombre = @heroe);

-- Para cargar los datos de tabla dota_heroes_abilities_o.csv
LOAD DATA INFILE '/var/www/webscraping.local/src/scraping/habilidades/dota_heroes_abilities_o.csv'
INTO TABLE habilidades
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@id_habilidad, @id_heroe, @heroe, nombre_habilidad, descripcion, imagen)
SET id_heroe = (SELECT id_heroe FROM heroes WHERE nombre = @heroe);

-- Probar si los datos relacionados funcionan:
SELECT * FROM heroes LIMIT 10;

SELECT h.nombre, p.popularidad, p.porcentaje_victoria, p.resultado 
FROM perfil_heroes p
JOIN heroes h ON p.id_heroe = h.id_heroe
LIMIT 10;


SELECT h.nombre, hb.nombre_habilidad, hb.descripcion, hb.imagen 
FROM habilidades hb
JOIN heroes h ON hb.id_heroe = h.id_heroe
WHERE h.nombre = 'Alchemist';


SELECT h.nombre, COUNT(hb.id_habilidad) AS total_habilidades
FROM heroes h
LEFT JOIN habilidades hb ON h.id_heroe = hb.id_heroe
GROUP BY h.id_heroe
ORDER BY total_habilidades DESC;

SELECT h.nombre, p.popularidad, p.porcentaje_victoria, p.resultado, hb.nombre_habilidad, hb.descripcion
FROM heroes h
LEFT JOIN perfil_heroes p ON h.id_heroe = p.id_heroe
LEFT JOIN habilidades hb ON h.id_heroe = hb.id_heroe
WHERE h.nombre = 'Axe';

SELECT h.nombre
FROM heroes h
LEFT JOIN habilidades hb ON h.id_heroe = hb.id_heroe
WHERE hb.id_habilidad IS NULL;


-- Probar Objetos para insertarlos
drop table if exists objetos;
CREATE TABLE objetos (
    id_item INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(255),
    Link VARCHAR(500)
);

-- hay cambiar algunas cosas:
-- Eliminar la clave foránea en objetos_descripcion
-- Como id_item en objetos está referenciado en objetos_descripcion, primero debemos eliminar la clave foránea antes de modificar la estructura de la tabla.
-- Ejecuta este comando para ver el nombre de la clave foránea:
SHOW CREATE TABLE objetos_descripcion;

-- quitamos la foreign key de la tabla objetos_descripcion
ALTER TABLE objetos_descripcion DROP FOREIGN KEY objetos_descripcion_ibfk_1;

-- Eliminar la clave primaria en objetos
ALTER TABLE objetos DROP PRIMARY KEY;

-- Modificar id_item para agregar AUTO_INCREMENT y volver a establecerla como PRIMARY KEY
ALTER TABLE objetos MODIFY id_item INT AUTO_INCREMENT PRIMARY KEY;

-- Volver a agregar la clave foránea en objetos_descripcion
ALTER TABLE objetos_descripcion ADD CONSTRAINT fk_objetos FOREIGN KEY (id_item) REFERENCES objetos(id_item) ON DELETE CASCADE;

drop table if exists objetos_descripcion;
CREATE TABLE objetos_descripcion (
    id_item INT PRIMARY KEY,
    Nombre VARCHAR(255),
    Imagen VARCHAR(500),
    Costo VARCHAR(255),
    Descripcion TEXT,
    FOREIGN KEY (id_item) REFERENCES objetos(id_item) ON DELETE CASCADE
);
--portatil
LOAD DATA INFILE '/var/lib/mysql-files/dota_items.csv'
INTO TABLE objetos
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- escritorio
LOAD DATA INFILE '/var/www/webscraping.local/src/scraping/objetos/dota_items.csv'
INTO TABLE objetos
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

--portatil
LOAD DATA INFILE '/var/lib/mysql-files/item_cleaned_for_mysql.csv'
INTO TABLE objetos_descripcion
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

--escritorio
LOAD DATA INFILE '/var/www/webscraping.local/src/scraping/objetos-description/item_cleaned_for_mysql.csv'
INTO TABLE objetos_descripcion
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;



