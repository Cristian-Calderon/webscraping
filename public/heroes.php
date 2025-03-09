<?php
session_start();

// Si el usuario no está autenticado, redirigir al login
if (!isset($_SESSION['user_id'])) {
    header("Location: /login");
    exit();
}

// Cargar Twig
require_once '../vendor/autoload.php';
$loader = new \Twig\Loader\FilesystemLoader('../templates');
$twig = new \Twig\Environment($loader);

// Renderizar la página de héroes
echo $twig->render('heroes.html.twig', [
    'username' => $_SESSION['username'],
    'email' => $_SESSION['email'],
    'user_id' => $_SESSION['user_id']
]);
?>
