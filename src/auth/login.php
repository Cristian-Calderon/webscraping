<?php
require './config.php';
require '../../vendor/autoload.php';

use Firebase\JWT\JWT;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'];
    $password = $_POST['password'];

    // Buscar el usuario en la base de datos
    $stmt = $pdo->prepare('SELECT * FROM users WHERE email = ?');
    $stmt->execute([$email]);
    $user = $stmt->fetch();

    if (!$user) {
        die('❌ Error: Usuario no encontrado.');
    }

    // Depuración: Mostrar los valores obtenidos
    echo "📌 Email ingresado: " . htmlspecialchars($email) . "<br>";
    echo "📌 Contraseña ingresada: " . htmlspecialchars($password) . "<br>";
    echo "📌 Hash almacenado en BD: " . htmlspecialchars($user['password']) . "<br>";

    // Comprobar si la contraseña ingresada coincide con la almacenada
    if (!password_verify($password, $user['password'])) {
        echo "❌ Error: La contraseña NO coincide.<br>";
        var_dump(password_verify($password, $user['password'])); // Depuración
        exit();
    }

    echo "✅ Contraseña correcta.<br>";

    // Generar el JWT si todo está correcto
    $payload = [
        'iss' => 'http://webscraping.local',
        'aud' => 'http://webscraping.local',
        'iat' => time(),
        'exp' => time() + (60 * 60), // 1 hora de duración
        'sub' => $user['id'],
    ];

    $jwt = JWT::encode($payload, $jwt_secret, 'HS256');

    // Guardar el token en una cookie segura
    setcookie("auth_token", $jwt, [
        "expires" => time() + (60 * 60),
        "path" => "/",
        "httponly" => true, // Evita acceso desde JavaScript
        "samesite" => "Strict"
    ]);

    echo "✅ Token generado correctamente: " . htmlspecialchars($jwt) . "<br>";

    // Redirigir al dashboard
    header('Location: /dashboard.php');
    exit();
}