<?php
require __DIR__ . '/../src/auth/config.php';


$email = 'cristian@cristian.com';

// Obtener la contraseña almacenada en la base de datos
$stmt = $pdo->prepare('SELECT password FROM users WHERE email = ?');
$stmt->execute([$email]);
$user = $stmt->fetch();

if (!$user) {
    die('❌ Error: Usuario no encontrado.');
}

$hashed_password = $user['password'];
$input_password = 'cristian'; // La contraseña que usaste en el registro

echo "📌 Contraseña ingresada: " . htmlspecialchars($input_password) . "<br>";
echo "📌 Hash almacenado: " . htmlspecialchars($hashed_password) . "<br>";

// Verificar la contraseña
if (password_verify($input_password, $hashed_password)) {
    echo "✅ La contraseña es válida.";
} else {
    echo "❌ Error: La contraseña no coincide.";
}
?>
