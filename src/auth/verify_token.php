<?php
require './config.php';
require '../../vendor/autoload.php';

use Firebase\JWT\JWT;
use Firebase\JWT\Key;

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $authHeader = $_SERVER['HTTP_AUTHORIZATION'] ?? '';

    if (!preg_match('/Bearer\s(\S+)/', $authHeader, $matches)) {
        http_response_code(400);
        die('Token no proporcionado o formato inválido.');
    }

    $token = $matches[1];

    try {
        $decoded = JWT::decode($token, new Key($jwt_secret, 'HS256'));
        echo json_encode(['user_id' => $decoded->sub]);
    } catch (Exception $e) {
        http_response_code(401);
        die('Token inválido: ' . $e->getMessage());
    }
}
