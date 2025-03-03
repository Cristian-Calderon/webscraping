<?php
require './config.php';
require '../../vendor/autoload.php';

use Firebase\JWT\JWT;
use Firebase\JWT\Key;

if (!isset($_COOKIE['auth_token'])) {
    http_response_code(401);
    die('Acceso no autorizado.');
}

$token = $_COOKIE['auth_token'];

try {
    $decoded = JWT::decode($token, new Key($jwt_secret, 'HS256'));
    echo json_encode(['user_id' => $decoded->sub]);
} catch (Exception $e) {
    http_response_code(401);
    die('Token inválido: ' . $e->getMessage());
}
