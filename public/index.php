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
    'admin' => 'admin.html.twig'
];

// 🔹 Si la ruta es "admin/delete/{id}", procesar la eliminación
if (preg_match('/^admin\/delete\/(\d+)$/', $request_uri, $matches)) {
    if (!isset($_COOKIE['auth_token'])) {
        die("❌ No autorizado.");
    }

    $token = $_COOKIE['auth_token'];
    try {
        $decoded = JWT::decode($token, new Key($jwt_secret, 'HS256'));
        $user_id = $decoded->sub;

        // Verificar si el usuario autenticado es admin
        $stmt = $pdo->prepare('SELECT role FROM users WHERE id = ?');
        $stmt->execute([$user_id]);
        $user = $stmt->fetch();

        if (!$user || $user['role'] !== 'admin') {
            die("❌ No tienes permisos para eliminar usuarios.");
        }

        // Obtener el ID del usuario a eliminar desde la URL
        $delete_id = $matches[1];

        // Evitar que un admin se elimine a sí mismo
        if ($delete_id == $user_id) {
            die("❌ No puedes eliminar tu propia cuenta.");
        }

        // Eliminar el usuario de la base de datos
        $stmt = $pdo->prepare('DELETE FROM users WHERE id = ?');
        $stmt->execute([$delete_id]);

        // Redirigir de vuelta al panel de administración
        header('Location: /admin');
        exit();

    } catch (Exception $e) {
        die("❌ Token inválido.");
    }
}

// 🔹 Si la ruta es "dashboard" o "admin", validar autenticación
if ($request_uri === 'dashboard' || $request_uri === 'admin') {
    if (!isset($_COOKIE['auth_token'])) {
        header('Location: /login');
        exit();
    }

    $token = $_COOKIE['auth_token'];
    try {
        $decoded = JWT::decode($token, new Key($jwt_secret, 'HS256'));
        $user_id = $decoded->sub;

        // Obtener datos del usuario
        $stmt = $pdo->prepare('SELECT username, email, role FROM users WHERE id = ?');
        $stmt->execute([$user_id]);
        $user = $stmt->fetch();

        if (!$user) {
            die("❌ Error: Usuario no encontrado.");
        }

        // 🔹 Si la ruta es "admin", verificar que el usuario sea admin
        if ($request_uri === 'admin') {
            if ($user['role'] !== 'admin') {
                die("❌ Acceso denegado. Solo administradores pueden acceder.");
            }

            // Obtener la lista de usuarios
            $stmt = $pdo->query('SELECT id, username, email, role FROM users');
            $users = $stmt->fetchAll();

            // Renderizar la página de administración
            echo $twig->render('admin.html.twig', [
                'username' => $user['username'],
                'email' => $user['email'],
                'role' => $user['role'],
                'users' => $users
            ]);
            exit();
        }

        // Renderizar el dashboard con los datos del usuario (Ahora incluye el rol)
        echo $twig->render('dashboard.html.twig', [
            'username' => $user['username'],
            'email' => $user['email'],
            'user_id' => $user_id,
            'role' => $user['role'] // 🔹 Ahora Twig sabe si el usuario es admin
        ]);
        exit();

    } catch (Exception $e) {
        header('Location: /login');
        exit();
    }
}

// 🔹 Si la ruta existe en el array de rutas, renderizar la página
if (array_key_exists($request_uri, $routes)) {
    echo $twig->render($routes[$request_uri]);
} else {
    // 🔹 Si la ruta no existe, mostrar error en lugar de 404
    http_response_code(404);
    die("❌ Error: La ruta '" . htmlspecialchars($request_uri) . "' no existe en el sistema.");
}
?>
