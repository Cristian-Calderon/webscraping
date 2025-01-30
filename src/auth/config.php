<?php
$host = 'localhost';
$db   = 'webscraping';
$user = 'cris';
$pass = '11011993';
$charset = 'utf8mb4';

$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];

try {
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (PDOException $e) {
    die('Connection failed: ' . $e->getMessage());
}

$jwt_secret = "EyYqUxGhXFA4cagM5Qb6vaivpR18UzY2NXj4YTN7nEaMxfUGR00a0KoCuTZlbrLb
KcjUuyBdV9cOO00P6XUbaw=="; // Cambia esto por una clave secreta segura.
