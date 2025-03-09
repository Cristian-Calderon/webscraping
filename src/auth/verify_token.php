<?php
require_once __DIR__ . '/config.php';
require '../../vendor/autoload.php';

use Firebase\JWT\JWT;
use Firebase\JWT\Key;

function verifyToken() {
    $headers = getallheaders();
    $token = $_COOKIE['auth_token'] ?? ($headers['Authorization'] ?? null);

    if (!$token) {
        http_response_code(401);
        die(json_encode(["error" => "Acceso no autorizado. Token no encontrado."]));
    }

    try {
        $decoded = JWT::decode(str_replace("Bearer ", "", $token), new Key($GLOBALS['jwt_secret'], 'HS256'));
        return $decoded->sub; // Retorna el ID del usuario autenticado
    } catch (Exception $e) {
        http_response_code(401);
        die(json_encode(["error" => "Token inválido o expirado."]));
    }
}
?>
