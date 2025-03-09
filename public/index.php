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
    'dashboard' => 'dashboard.html.twig',
    'admin' => 'admin.html.twig',
    'heroes' => 'heroes.html.twig'
];

// 🔹 Validación de autenticación para rutas protegidas
if ($request_uri === 'heroes') {
    $token = $_COOKIE['auth_token'] ?? null;
    if (!$token) {
        die("❌ DEBUG: No hay token en la cookie. Redirigiendo a login.");
    }
    
    try {
        $decoded = JWT::decode($token, new Key($jwt_secret, 'HS256'));
        $user_id = $decoded->sub;
        error_log("✅ DEBUG: Token válido. Usuario ID: " . $user_id);

        // Obtener datos del usuario desde la BD
        $stmt = $pdo->prepare('SELECT username, email, role FROM users WHERE id = ?');
        $stmt->execute([$user_id]);
        $user = $stmt->fetch();

        if (!$user) {
            die("❌ DEBUG: Usuario no encontrado en la base de datos.");
        }

        // Verificar si `heroes.html.twig` existe
        if (!file_exists(__DIR__ . "/templates/heroes.html.twig")) {
            die("❌ DEBUG: Archivo heroes.html.twig no encontrado.");
        }

        // Renderizar la página
        echo $twig->render('heroes.html.twig', [
            'username' => $user['username'],
            'email' => $user['email'],
            'user_id' => $user_id,
            'role' => $user['role']
        ]);
        exit();
    } catch (Exception $e) {
        die("❌ DEBUG: Error al decodificar el token: " . $e->getMessage());
    }
}

// 🔹 Renderizar la página si la ruta existe
if (array_key_exists($request_uri, $routes)) {
    error_log("DEBUG: Renderizando página pública de $request_uri.");
    echo $twig->render($routes[$request_uri]);
} else {
    http_response_code(404);
    error_log("DEBUG: Ruta no encontrada: $request_uri");
    die("❌ Error: La ruta '" . htmlspecialchars($request_uri) . "' no existe en el sistema.");
}

// Función de depuración para registrar errores
function debug_log($message) {
    error_log("DEBUG: " . $message);
}
?>