
-- 6 de Marzo actualizado:
CREATE TABLE heroes (
    id_heroe INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL,
    link_imagen TEXT,
    link_pagina TEXT
);


-- Como insertar datos:
LOAD DATA INFILE '/var/www/webscraping.local/src/scraping/heroes/heroes-spanish.csv'
INTO TABLE heroes
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS (nombre, link_imagen, link_pagina);


-- 2da tabla:
CREATE TABLE perfil_heroes (
    id_perfil INT AUTO_INCREMENT PRIMARY KEY,
    id_heroe INT NOT NULL,
    popularidad VARCHAR(50),
    porcentaje_victoria DECIMAL(5,2),
    fuerza VARCHAR(50),
    agilidad VARCHAR(50),
    inteligencia VARCHAR(50),
    velocidad_movimiento INT,
    rango_vision VARCHAR(50),
    armadura DECIMAL(5,2),
    tiempo_ataque_base DECIMAL(5,2),
    daño VARCHAR(50),
    punto_ataque DECIMAL(5,2),
    FOREIGN KEY (id_heroe) REFERENCES heroes(id_heroe) ON DELETE CASCADE
);
-- 🔹 1. Asegurar que la tabla temporal no existe
DROP TEMPORARY TABLE IF EXISTS perfil_heroes_temp;
--🔹 2. Crear la tabla temporal correctamente
CREATE TEMPORARY TABLE perfil_heroes_temp LIKE perfil_heroes;
-- 🔹 3. Agregar la columna Heroe para la carga temporal
ALTER TABLE perfil_heroes_temp 
ADD COLUMN Heroe VARCHAR(255) AFTER id_perfil;



-- 📌 4. Cargar Datos en la Tabla Temporal
LOAD DATA LOCAL INFILE '/var/www/webscraping.local/src/scraping/perfil-mejorado/dota_heroes_data.csv'
INTO TABLE perfil_heroes_temp
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Heroe, Popularidad, Porcentaje_de_Victoria, Resultado, Fuerza, Agilidad, Inteligencia, Velocidad_de_movimiento, Rango_de_vision, Armadura, Tiempo_de_Ataque_Base, Damage, Punto_de_ataque);

-- 📌 Verifica que los datos se insertaron correctamente:
SELECT * FROM perfil_heroes_temp LIMIT 5;

-- 📌 5. Asignar id_heroe en perfil_heroes_temp
UPDATE perfil_heroes_temp p
JOIN heroes h ON p.Heroe = h.nombre
SET p.id_heroe = h.id_heroe;

-- 📌 6. Insertar los Datos en perfil_heroes
INSERT INTO perfil_heroes (id_heroe, Popularidad, Porcentaje_de_Victoria, Resultado, Fuerza, Agilidad, Inteligencia, Velocidad_de_movimiento, Rango_de_vision, Armadura, Tiempo_de_Ataque_Base, Damage, Punto_de_ataque)
SELECT id_heroe, Popularidad, Porcentaje_de_Victoria, Resultado, Fuerza, Agilidad, Inteligencia, Velocidad_de_movimiento, Rango_de_vision, Armadura, Tiempo_de_Ataque_Base, Damage, Punto_de_ataque
FROM perfil_heroes_temp;

-- 📌 7. Eliminar la Tabla Temporal
DROP TEMPORARY TABLE perfil_heroes_temp;







------------------------------ 3era tabla
---📌 1. Verificar la Estructura de habilidades
-- Primero, asegurémonos de que la tabla habilidades tiene la estructura correcta y que id_heroe está relacionado con la tabla heroes.
DROP TABLE IF EXISTS habilidades;

CREATE TABLE habilidades (
    id_habilidad INT AUTO_INCREMENT PRIMARY KEY,
    id_heroe INT NOT NULL,
    nombre_habilidad VARCHAR(255),
    descripcion TEXT,
    imagen TEXT,
    FOREIGN KEY (id_heroe) REFERENCES heroes(id_heroe) ON DELETE CASCADE
);



--📌 2. Crear una Tabla Temporal (habilidades_temp)
DROP TEMPORARY TABLE IF EXISTS habilidades_temp;

CREATE TEMPORARY TABLE habilidades_temp (
    id_habilidad INT,
    Heroe VARCHAR(255),  -- Temporalmente usaremos 'Heroe' en lugar de 'id_heroe'
    nombre_habilidad VARCHAR(255),
    descripcion TEXT,
    imagen TEXT,
    id_heroe INT  -- Se agregará después para relacionarlo con 'heroes'
);


---📌 3. Cargar el CSV en habilidades_temp
LOAD DATA LOCAL INFILE '/var/www/webscraping.local/src/scraping/habilidades/dota_heroes_abilities_o.csv'
INTO TABLE habilidades_temp
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'  
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id_habilidad, id_heroe, Heroe, nombre_habilidad, descripcion, imagen);



-- 📌 4. Verificar los Datos Cargados
SELECT id_habilidad, nombre_habilidad, descripcion, imagen FROM habilidades_temp LIMIT 10;

UPDATE habilidades_temp h
JOIN heroes he ON h.Heroe = he.nombre
SET h.id_heroe = he.id_heroe;

SELECT HEX(Heroe) FROM habilidades_temp LIMIT 10;

UPDATE habilidades_temp 
SET Heroe = TRIM(Heroe);

INSERT INTO habilidades (id_habilidad, id_heroe, nombre_habilidad, descripcion, imagen)
SELECT id_habilidad, id_heroe, nombre_habilidad, descripcion, imagen
FROM habilidades_temp;
sss

--📌 📌 7. Eliminar la Tabla Temporal
DROP TEMPORARY TABLE habilidades_temp;




--------------- objetos

CREATE TABLE objetos (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL,
    link_pagina TEXT
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



CREATE TABLE objetos_descripcion (
    id_objeto INT AUTO_INCREMENT PRIMARY KEY,
    id_item INT NOT NULL,
    imagen TEXT,
    costo INT,
    descripcion TEXT,
    FOREIGN KEY (id_item) REFERENCES objetos(id_item) ON DELETE CASCADE
);


-- insert objetos.csv
LOAD DATA LOCAL INFILE '/ruta/donde/esta/objetos.csv'
INTO TABLE objetos
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id_item, nombre, link_pagina);



-- insert objetos_descripcion.csv

LOAD DATA LOCAL INFILE '/ruta/donde/esta/objetos-description.csv'
INTO TABLE objetos_descripcion
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id_item, nombre, imagen, costo, descripcion);
