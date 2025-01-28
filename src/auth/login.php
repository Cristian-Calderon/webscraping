<?php
require './config.php';
require '../../vendor/autoload.php';

use Firebase\JWT\JWT;
use Firebase\JWT\Key;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'];
    $password = $_POST['password'];

    $stmt = $pdo->prepare('SELECT * FROM users WHERE email = ?');
    $stmt->execute([$email]);
    $user = $stmt->fetch();

    if ($user && password_verify($password, $user['password'])) {
        $payload = [
            'iss' => 'http://webscraping.local',
            'aud' => 'http://webscraping.local',
            'iat' => time(),
            'exp' => time() + (60 * 60), // 1 hora de duración
            'sub' => $user['id'],
        ];

        $jwt = JWT::encode($payload, $jwt_secret, 'HS256');
        echo json_encode(['token' => $jwt]);
    } else {
        http_response_code(401);
        echo 'Credenciales incorrectas.';
    }
}
