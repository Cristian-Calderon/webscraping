<?php

// require_once __DIR__ . '/vendor/autoload.php';
require_once "../vendor/autoload.php";


// $loader = new \Twig\Loader\FilesystemLoader(__DIR__ . '/templates');
$loader = new \Twig\Loader\FilesystemLoader('./templates');

// $twig = new \Twig\Environment($loader, [
//     'cache' => __DIR__ . '/cache', // Opcional, para usar caché de Twig
// ]);

$twig = new \Twig\Environment($loader, [
    //	'cache' => 'cache',
    ]);


echo $twig->render('index.html.twig', ['name' => 'Cristian']);

?>