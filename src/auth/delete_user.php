<?php
require '../../vendor/autoload.php';
require '../../auth/config.php';

session_start();

if (!isset($_COOKIE['auth_token'])) {
    die("❌ No autorizado.");
}

$token = $_COOKIE['auth_token'];

try {
    $decoded = JWT::decode($token, new Key($jwt_secret, 'HS256'));
    $user_id = $decoded->sub;

    $stmt = $pdo->prepare('SELECT role FROM users WHERE id = ?');
    $stmt->execute([$user_id]);
    $user = $stmt->fetch();

    if ($user['role'] !== 'admin') {
        die("❌ No tienes permisos.");
    }

    $id = $_GET['id'];
    $stmt = $pdo->prepare('DELETE FROM users WHERE id = ?');
    $stmt->execute([$id]);

    header('Location: /admin');
    exit();

} catch (Exception $e) {
    die("❌ Token inválido.");
}
?>
