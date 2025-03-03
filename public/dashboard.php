<?php

require __DIR__ . '/auth/config.php';
require __DIR__ . '/../vendor/autoload.php';

use Firebase\JWT\JWT;
use Firebase\JWT\Key;

session_start();

// Verificar si el token está en la cookie
if (!isset($_COOKIE['auth_token'])) {
    header('Location: /login');
    exit();
}

$token = $_COOKIE['auth_token'];

try {
    $decoded = JWT::decode($token, new Key($jwt_secret, 'HS256'));
    $user_id = $decoded->sub;

    // Obtener los datos del usuario desde la base de datos
    $stmt = $pdo->prepare('SELECT username, email FROM users WHERE id = ?');
    $stmt->execute([$user_id]);
    $user = $stmt->fetch();

    if (!$user) {
        die("❌ Error: Usuario no encontrado.");
    }

} catch (Exception $e) {
    header('Location: /login');
    exit();
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard | WebScraping</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">

    <!-- Barra de navegación -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">WebScraping</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/home">Inicio</a></li>
                    <li class="nav-item"><a class="nav-link" href="/dashboard.php">Dashboard</a></li>
                    <li class="nav-item"><a class="nav-link btn btn-danger text-white" href="/logout.php">Cerrar sesión</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Contenido del dashboard -->
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card shadow-lg">
                    <div class="card-header bg-primary text-white text-center">
                        <h2>Bienvenido al Dashboard</h2>
                    </div>
                    <div class="card-body text-center">
                        <h4 class="text-success">Hola, <?= htmlspecialchars($user['username']) ?>!</h4>
                        <p class="text-muted">Tu correo: <?= htmlspecialchars($user['email']) ?></p>
                        <p>Tu ID de usuario es: <strong><?= htmlspecialchars($user_id) ?></strong></p>
                        <a href="./logout.php" class="btn btn-danger mt-3">Cerrar sesión</a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Pie de página -->
    <footer class="bg-dark text-white text-center py-3 mt-5">
        <p>&copy; 2024 WebScraping. Todos los derechos reservados.</p>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html