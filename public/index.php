<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

require __DIR__ . '/auth/config.php';
require __DIR__ . '/../vendor/autoload.php';

use Firebase\JWT\JWT;
use Firebase\JWT\Key;

// Configurar Twig con la carpeta de templates
$templatesPath = realpath(__DIR__ . '/templates');
if (!$templatesPath || !is_dir($templatesPath)) {
    die("Error: La carpeta templates NO EXISTE en " . __DIR__ . '/templates');
}

$loader = new \Twig\Loader\FilesystemLoader($templatesPath);
$twig = new \Twig\Environment($loader, [
    //'cache' => __DIR__ . '/../cache',
]);

// Obtener la ruta actual desde $_GET['route']
$request_uri = $_GET['route'] ?? 'home'; // Si no hay ruta, se carga "home"

// Mapeo de rutas a sus respectivos archivos Twig
$routes = [
    'home' => 'home.html.twig',
    'register' => 'register.html.twig',
    'login' => 'login.html.twig',
    'dashboard' => 'dashboard.html.twig' // Asegurar que esta línea existe
];

// Si la ruta es el dashboard, validar autenticación
if ($request_uri === 'dashboard') {
    if (!isset($_COOKIE['auth_token'])) {
        header('Location: /login');
        exit();
    }

    $token = $_COOKIE['auth_token'];
    try {
        $decoded = JWT::decode($token, new Key($jwt_secret, 'HS256'));
        $user_id = $decoded->sub;

        // Obtener datos del usuario
        $stmt = $pdo->prepare('SELECT username, email FROM users WHERE id = ?');
        $stmt->execute([$user_id]);
        $user = $stmt->fetch();

        if (!$user) {
            die("❌ Error: Usuario no encontrado.");
        }

        // Renderizar el dashboard con los datos del usuario
        echo $twig->render('dashboard.html.twig', [
            'username' => $user['username'],
            'email' => $user['email'],
            'user_id' => $user_id
        ]);
        exit();

    } catch (Exception $e) {
        header('Location: /login');
        exit();
    }
}

// Si la ruta existe en el array de rutas, renderizar la página
if (array_key_exists($request_uri, $routes)) {
    echo $twig->render($routes[$request_uri]);
} else {
    // Si la ruta no existe, mostrar error en lugar de 404
    http_response_code(404);
    die("❌ Error: La ruta '" . htmlspecialchars($request_uri) . "' no existe en el sistema.");
}
?>
