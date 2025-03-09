<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

header("Content-Type: application/json");
require_once __DIR__ . '/../src/auth/config.php';
require_once __DIR__ . '/../src/auth/verify_token.php';

// Conectar a la base de datos
try {
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (PDOException $e) {
    echo json_encode(["error" => "Error de conexión a la base de datos", "message" => $e->getMessage()]);
    exit;
}

// Verificar si se proporciona un ID de héroe
if (!isset($_GET['id_heroe'])) {
    echo json_encode(["error" => "ID de héroe requerido"]);
    exit;
}

$id_heroe = (int) $_GET['id_heroe']; // Convertir a número para mayor seguridad

// Verificar que el héroe exista
$stmt = $pdo->prepare("SELECT COUNT(*) FROM heroes WHERE id_heroe = ?");
$stmt->execute([$id_heroe]);
if ($stmt->fetchColumn() == 0) {
    echo json_encode(["error" => "Héroe no encontrado"]);
    exit;
}

// Obtener habilidades del héroe
$stmt = $pdo->prepare("SELECT * FROM habilidades WHERE id_heroe = ?");
$stmt->execute([$id_heroe]);
$habilidades = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Verificar si hay habilidades
if ($habilidades) {
    echo json_encode($habilidades);
} else {
    echo json_encode(["error" => "No se encontraron habilidades para este héroe"]);
}
?>
