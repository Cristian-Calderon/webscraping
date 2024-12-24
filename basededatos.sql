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