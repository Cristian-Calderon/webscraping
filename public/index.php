<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once "../vendor/autoload.php";

// Configurar Twig con la carpeta de templates
$templatesPath = realpath(__DIR__ . '/templates');
if (!$templatesPath || !is_dir($templatesPath)) {
    die("Error: La carpeta templates NO EXISTE en " . __DIR__ . '/templates');
}

$loader = new \Twig\Loader\FilesystemLoader($templatesPath);
$twig = new \Twig\Environment($loader, [
    //'cache' => __DIR__ . '/../cache',
]);

// Obtener la ruta actual desde $_GET['route'] (modificada por .htaccess)
$request_uri = $_GET['route'] ?? 'home'; // Si no hay ruta, se carga "home"

// Mapeo de rutas a sus respectivos archivos Twig
$routes = [
    'home' => 'home.html.twig',
    'register' => 'register.html.twig',
    'login' => 'login.html.twig'
];

// Verificar si la ruta existe en el array de rutas
if (array_key_exists($request_uri, $routes)) {
    echo $twig->render($routes[$request_uri]);
} else {
    // Si la ruta no existe, mostrar 404
    http_response_code(404);
    echo $twig->render('404.html.twig');
}
