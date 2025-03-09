<?php
require '../auth/config.php';
require '../../vendor/autoload.php';

use Firebase\JWT\JWT;
use Firebase\JWT\Key;

// Verificar autenticación
$token = $_COOKIE['auth_token'] ?? null;
if (!$token) {
    die(json_encode(["error" => "No autorizado."]));
}

try {
    $decoded = JWT::decode($token, new Key($jwt_secret, 'HS256'));
    $user_id = $decoded->sub;
} catch (Exception $e) {
    die(json_encode(["error" => "Token inválido."]));
}

// Conectar a la base de datos
$pdo = new PDO("mysql:host=$db_host;dbname=$db_name", $db_user, $db_pass);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'GET') {
    // Obtener habilidades
    $stmt = $pdo->query("SELECT * FROM habilidades");
    $habilidades = $stmt->fetchAll(PDO::FETCH_ASSOC);
    echo json_encode($habilidades);
} elseif ($method === 'POST') {
    // Agregar una nueva habilidad
    $data = json_decode(file_get_contents("php://input"), true);
    if (!isset($data['nombre'])) {
        die(json_encode(["error" => "Nombre requerido"]));
    }
    
    $stmt = $pdo->prepare("INSERT INTO habilidades (nombre) VALUES (?)");
    $stmt->execute([$data['nombre']]);
    echo json_encode(["success" => "Habilidad agregada"]);
} elseif ($method === 'PUT') {
    // Actualizar habilidad
    $data = json_decode(file_get_contents("php://input"), true);
    if (!isset($data['id']) || !isset($data['nombre'])) {
        die(json_encode(["error" => "ID y Nombre requeridos"]));
    }

    $stmt = $pdo->prepare("UPDATE habilidades SET nombre = ? WHERE id = ?");
    $stmt->execute([$data['nombre'], $data['id']]);
    echo json_encode(["success" => "Habilidad actualizada"]);
} elseif ($method === 'DELETE') {
    // Eliminar habilidad
    $data = json_decode(file_get_contents("php://input"), true);
    if (!isset($data['id'])) {
        die(json_encode(["error" => "ID requerido"]));
    }

    $stmt = $pdo->prepare("DELETE FROM habilidades WHERE id = ?");
    $stmt->execute([$data['id']]);
    echo json_encode(["success" => "Habilidad eliminada"]);
} else {
    http_response_code(405);
    echo json_encode(["error" => "Método no permitido"]);
}
?>
