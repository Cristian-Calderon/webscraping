<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

header("Content-Type: application/json");
require_once __DIR__ . '/../auth/config.php'; // Archivo con conexión a la BD
require_once __DIR__ . '/../auth/verify_token.php'; // Verifica autenticación con JWT

// DEPURACIÓN: Mostrar qué está capturando Apache
$requestUri = trim(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH), '/');
$scriptName = trim(dirname($_SERVER['SCRIPT_NAME']), '/');

error_log("DEBUG: REQUEST_URI = " . $_SERVER['REQUEST_URI']);
error_log("DEBUG: SCRIPT_NAME = " . $_SERVER['SCRIPT_NAME']);
error_log("DEBUG: requestUri = " . $requestUri);
error_log("DEBUG: scriptName = " . $scriptName);

$basePath = $scriptName;
if (!empty($basePath) && strpos($requestUri, $basePath) === 0) {
    $requestUri = substr($requestUri, strlen($basePath));
}

$path = explode('/', trim($requestUri, '/'));
error_log("DEBUG: path = " . print_r($path, true));

// Validar si la ruta es correcta
if (count($path) < 1 || strpos($path[0], 'heroes') === false) {

    http_response_code(404);
    echo json_encode(["error" => "Endpoint no encontrado", "debug" => $path]);
    exit;
}

// Conectar a la base de datos
try {
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (PDOException $e) {
    echo json_encode(["error" => "Error de conexión a la base de datos", "message" => $e->getMessage()]);
    exit;
}

// Manejo de solicitudes HTTP
$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case 'GET':
        if (isset($_GET['id'])) {
            $stmt = $pdo->prepare("SELECT * FROM heroes WHERE id_heroe = ?");
            $stmt->execute([$_GET['id']]);
            $hero = $stmt->fetch(PDO::FETCH_ASSOC);
            echo json_encode($hero ?: ["error" => "Héroe no encontrado"]);
        } else {
            $stmt = $pdo->query("SELECT * FROM heroes");
            echo json_encode($stmt->fetchAll(PDO::FETCH_ASSOC));
        }
        break;
    
    case 'PUT':
    case 'DELETE':
        verifyToken(); // Verifica autenticación solo para métodos protegidos
        parse_str(file_get_contents("php://input"), $data);
        
        if ($method === 'PUT') {
            $stmt = $pdo->prepare("UPDATE heroes SET nombre = ?, link_img = ?, link_page = ? WHERE id_heroe = ?");
            $success = $stmt->execute([$data['nombre'], $data['link_img'], $data['link_page'], $_GET['id']]);
        } elseif ($method === 'DELETE') {
            $stmt = $pdo->prepare("DELETE FROM heroes WHERE id_heroe = ?");
            $success = $stmt->execute([$_GET['id']]);
        }
        echo json_encode(["success" => $success]);
        break;
    
    default:
        http_response_code(405);
        echo json_encode(["error" => "Método no permitido"]);
}
