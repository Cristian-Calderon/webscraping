CREATE DATABASE IF NOT EXISTS dotabuff_scraping;

USE dotabuff_scraping;

-- Tabla de Facetas
CREATE TABLE IF NOT EXISTS facetas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Tabla de Héroes
CREATE TABLE IF NOT EXISTS heroes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    faceta_id INT,
    nivel VARCHAR(12),
    tasa_victoria VARCHAR(12),
    tasa_seleccion VARCHAR(10),
    tasa_prohibicion VARCHAR(10),
    url_hero TEXT,
    FOREIGN KEY (faceta_id) REFERENCES facetas(id) ON DELETE SET NULL
);

-- Tabla de Usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    faceta_id INT,
    nivel VARCHAR(12),
    tasa_victoria VARCHAR(12),
    tasa_seleccion VARCHAR(10),
    tasa_prohibicion VARCHAR(10),
    url_hero TEXT,
    url_faceta TEXT,
    FOREIGN KEY (faceta_id) REFERENCES facetas(id) ON DELETE SET NULL
);

-- Tabla de relación Usuarios-Héroes
CREATE TABLE IF NOT EXISTS user_heroes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    hero_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (hero_id) REFERENCES heroes(id) ON DELETE CASCADE
);


-- 6 de Marzo actualizado:
CREATE TABLE heroes (
    id_heroe INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL,
    link_imagen TEXT,
    link_pagina TEXT
);

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

CREATE TABLE habilidades (
    id_habilidad INT AUTO_INCREMENT PRIMARY KEY,
    id_heroe INT NOT NULL,
    nombre_habilidad VARCHAR(255),
    descripcion TEXT,
    imagen TEXT,
    FOREIGN KEY (id_heroe) REFERENCES heroes(id_heroe) ON DELETE CASCADE
);

-- Como insertar datos:
LOAD DATA INFILE '/ruta/donde/subiste/heroes.csv'
INTO TABLE heroes
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS (nombre, link_imagen, link_pagina);

LOAD DATA INFILE '/ruta/donde/subiste/perfil_heroes.csv'
INTO TABLE perfil_heroes
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Héroe, Popularidad, Porcentaje_de_Victoria, Resultado, Fuerza, Agilidad, Inteligencia, Velocidad_de_movimiento, Rango_de_visión, Armadura, Tiempo_de_Ataque_Base, Daño, Punto_de_ataque);

LOAD DATA INFILE '/ruta/donde/subiste/habilidades.csv'
INTO TABLE habilidades
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id_habilidad, id_heroe, Héroe, Nombre_de_Habilidad, Descripción, Imagen);



--- objetos

CREATE TABLE objetos (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL,
    link_pagina TEXT
);

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
