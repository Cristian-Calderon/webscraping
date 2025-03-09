<?php
session_start();

if (!isset($_COOKIE['auth_token'])) {
    header("Location: /login");
    exit();
}

require_once '../vendor/autoload.php';
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

$jwt_secret = "TU_CLAVE_SECRETA"; // Usa la misma clave que en login.php

try {
    $decoded = JWT::decode($_COOKIE['auth_token'], new Key($jwt_secret, 'HS256'));
    $user_id = $decoded->sub;

    // Cargar Twig
    $loader = new \Twig\Loader\FilesystemLoader('../templates');
    $twig = new \Twig\Environment($loader);

    // Renderizar la página de héroes
    echo $twig->render('heroes.html.twig', ['user_id' => $user_id]);
} catch (Exception $e) {
    header("Location: /login");
    exit();
}
