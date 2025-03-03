<?php
require '../../vendor/autoload.php';
require '../../auth/config.php';

session_start();

if (!isset($_COOKIE['auth_token'])) {
    die("❌ No autorizado.");
}

$token = $_COOKIE['auth_token'];
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

try {
    $decoded = JWT::decode($token, new Key($jwt_secret, 'HS256'));
    $user_id = $decoded->sub;

    // Verificar si es admin
    $stmt = $pdo->prepare('SELECT role FROM users WHERE id = ?');
    $stmt->execute([$user_id]);
    $user = $stmt->fetch();

    if ($user['role'] !== 'admin') {
        die("❌ No tienes permisos.");
    }

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $id = $_POST['id'];
        $username = $_POST['username'];
        $email = $_POST['email'];
        $role = $_POST['role'];

        $stmt = $pdo->prepare('UPDATE users SET username = ?, email = ?, role = ? WHERE id = ?');
        $stmt->execute([$username, $email, $role, $id]);

        header('Location: /admin');
        exit();
    }

} catch (Exception $e) {
    die("❌ Token inválido.");
}
?>
