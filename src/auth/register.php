<?php
require './config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'];
    $password = $_POST['password'];
    $username = $_POST['username'];

    // Encriptar la contraseña antes de guardarla
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    // Depuración: Mostrar el hash generado para verificarlo
    echo "Contraseña encriptada: " . $hashed_password . "<br>";

    $stmt = $pdo->prepare('INSERT INTO users (username, email, password) VALUES (?, ?, ?)');
    try {
        $stmt->execute([$username, $email, $hashed_password]);
        echo 'Registro exitoso.';
    } catch (PDOException $e) {
        echo 'Error: ' . $e->getMessage();
    }
}
