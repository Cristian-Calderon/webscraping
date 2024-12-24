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

-- CONTENIDO DE PERFIL
-- Tabla de Usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,  [autogenera]
    name VARCHAR(50) NOT NULL,          [scraping] texto
    nivel VARCHAR(12),                  [scraping] medalla
    ultima_partida VARCHAR(10),         [scraping] texto
    tasa_victoria VARCHAR(12),          [scraping] numero 
    partidas_ganadas VARCHAR(10),       [scraping] numero
    partidas_perdidas VARCHAR(10),      [scraping] numero
    
);

-- Tabla Roles and Lineas
-- Otra tabla de relacion [Roles y Lineas]
create table if not exists roles_lineas (
    id_users INT,                       [relacion con users]
    core VARCHAR(10),                   [scraping] numero
    support VARCHAR(10),                [scraping] numero
);

-- Tabla most played heroes
create most_played_heroes (
    id_users INT,                       [relacion con users]
    hero_id INT,                        [relacion con heroes]
    partidas INT,                       [scraping] numero
    tasa_victoria VARCHAR(12),          [scraping] numero
    tasa_seleccion VARCHAR(10),         [scraping] numero
    tasa_prohibicion VARCHAR(10),       [scraping] numero
);



-- Crear la tabla url_match con url_match como UNIQUE
CREATE TABLE IF NOT EXISTS url_match (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url_match VARCHAR(255) UNIQUE -- Cambiado a VARCHAR
);

-- Crear la tabla last_matches con la clave foránea
CREATE TABLE IF NOT EXISTS last_matches (
    id_users INT,                       -- Relación con users
    hero_id INT,                        -- Relación con heroes
    resultado VARCHAR(10),              -- Scraping
    kda VARCHAR(10),                    -- Scraping
    duracion VARCHAR(10),               -- Scraping
    fecha VARCHAR(10),                  -- Scraping
    url_match VARCHAR(255),             -- Cambiado a VARCHAR
    FOREIGN KEY (url_match) REFERENCES url_match(url_match) ON DELETE CASCADE
);
