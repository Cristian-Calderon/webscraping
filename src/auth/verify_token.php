<?php
require_once __DIR__ . '/config.php';
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

function verifyToken() {
    if ($_SERVER['REQUEST_METHOD'] === 'PUT' || $_SERVER['REQUEST_METHOD'] === 'DELETE') {
        if (!isset($_SERVER['HTTP_AUTHORIZATION'])) {
            http_response_code(401);
            echo json_encode(["error" => "Acceso no autorizado"]);
            exit;
        }

        $authHeader = $_SERVER['HTTP_AUTHORIZATION'];
        $tokenParts = explode(' ', $authHeader);

        if (count($tokenParts) !== 2 || $tokenParts[0] !== 'Bearer') {
            http_response_code(401);
            echo json_encode(["error" => "Formato de token inválido"]);
            exit;
        }

        $token = $tokenParts[1];

        try {
            $decoded = JWT::decode($token, new Key(SECRET_KEY, 'HS256'));
            return $decoded;
        } catch (Exception $e) {
            http_response_code(401);
            echo json_encode(["error" => "Token inválido", "message" => $e->getMessage()]);
            exit;
        }
    }
}
