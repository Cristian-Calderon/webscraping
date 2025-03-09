<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

header("Content-Type: application/json");
require_once __DIR__ . '/../auth/config.php';  // ✅ Usa el link simbólico
require_once __DIR__ . '/../auth/verify_token.php';


// Conectar a la base de datos
try {
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (PDOException $e) {
    echo json_encode(["error" => "Error de conexión a la base de datos", "message" => $e->getMessage()]);
    exit;
}

// Detectar el tipo de solicitud
$method = $_SERVER['REQUEST_METHOD'];
$resource = $_GET['resource'] ?? null;
$id = $_GET['id'] ?? null;

// 🌟 Rutas disponibles en la API
switch ($resource) {
    case 'heroes':
        handleHeroes($method, $id, $pdo);
        break;

    case 'objetos':
        handleObjetos($method, $id, $pdo);
        break;

    default:
        http_response_code(404);
        echo json_encode(["error" => "Recurso no encontrado"]);
}

// ✅ Función para manejar Héroes (Crear, Leer, Editar, Eliminar)
function handleHeroes($method, $id, $pdo)
{
    switch ($method) {
        case 'GET': // Obtener héroe y sus datos relacionados
            if ($id) {
                $stmt = $pdo->prepare("SELECT * FROM heroes WHERE id_heroe = ?");
                $stmt->execute([$id]);
                $heroe = $stmt->fetch(PDO::FETCH_ASSOC);

                if (!$heroe) {
                    echo json_encode(["error" => "Héroe no encontrado"]);
                    return;
                }

                // Obtener habilidades
                $stmt = $pdo->prepare("SELECT * FROM habilidades WHERE id_heroe = ?");
                $stmt->execute([$id]);
                $heroe['habilidades'] = $stmt->fetchAll(PDO::FETCH_ASSOC);

                // Obtener perfil del héroe
                $stmt = $pdo->prepare("SELECT * FROM perfil_heroes WHERE id_heroe = ?");
                $stmt->execute([$id]);
                $heroe['perfil'] = $stmt->fetch(PDO::FETCH_ASSOC);

                echo json_encode($heroe);
            } else {
                // Obtener todos los héroes
                $stmt = $pdo->query("SELECT * FROM heroes");
                echo json_encode($stmt->fetchAll(PDO::FETCH_ASSOC));
            }
            break;

        case 'POST': // Crear un nuevo héroe con habilidades y perfil
            verifyToken();
            $data = json_decode(file_get_contents("php://input"), true);
            if (!isset($data['nombre'], $data['link_img'], $data['link_page'])) {
                echo json_encode(["error" => "Faltan datos para crear el héroe."]);
                return;
            }

            // Insertar Héroe
            $stmt = $pdo->prepare("INSERT INTO heroes (nombre, link_img, link_page) VALUES (?, ?, ?)");
            $stmt->execute([$data['nombre'], $data['link_img'], $data['link_page']]);
            $id_heroe = $pdo->lastInsertId();

            echo json_encode(["success" => "Héroe agregado", "id_heroe" => $id_heroe]);
            break;

        case 'PUT': // Editar héroe
            verifyToken();
            $data = json_decode(file_get_contents("php://input"), true);
            if (!isset($data['id'], $data['nombre'], $data['link_img'], $data['link_page'])) {
                echo json_encode(["error" => "Faltan datos para actualizar el héroe."]);
                return;
            }

            $stmt = $pdo->prepare("UPDATE heroes SET nombre = ?, link_img = ?, link_page = ? WHERE id_heroe = ?");
            $stmt->execute([$data['nombre'], $data['link_img'], $data['link_page'], $data['id']]);

            echo json_encode(["success" => "Héroe actualizado"]);
            break;

        case 'DELETE': // Eliminar héroe
            verifyToken();
            if (!$id) {
                echo json_encode(["error" => "ID de héroe requerido"]);
                return;
            }

            $stmt = $pdo->prepare("DELETE FROM heroes WHERE id_heroe = ?");
            $stmt->execute([$id]);

            echo json_encode(["success" => "Héroe eliminado"]);
            break;

        default:
            http_response_code(405);
            echo json_encode(["error" => "Método no permitido"]);
    }
}

// ✅ Función para manejar Objetos (Crear, Leer, Editar, Eliminar)
function handleObjetos($method, $id, $pdo)
{
    switch ($method) {
        case 'GET': // Obtener objetos y sus descripciones
            if ($id) {
                $stmt = $pdo->prepare("
                    SELECT o.id_item, o.Nombre, d.Imagen, d.Costo, d.Descripcion 
                    FROM objetos o 
                    LEFT JOIN objetos_descripcion d ON o.id_item = d.id_item
                    WHERE o.id_item = ?
                ");
                $stmt->execute([$id]);
                $objeto = $stmt->fetch(PDO::FETCH_ASSOC);

                if (!$objeto) {
                    echo json_encode(["error" => "Objeto no encontrado"]);
                    return;
                }

                echo json_encode($objeto);
            } else {
                // Obtener todos los objetos con su imagen
                $stmt = $pdo->query("
                    SELECT o.id_item, o.Nombre, d.Imagen 
                    FROM objetos o 
                    LEFT JOIN objetos_descripcion d ON o.id_item = d.id_item
                ");
                echo json_encode($stmt->fetchAll(PDO::FETCH_ASSOC));
            }
            break;

        case 'POST': // Crear un nuevo objeto
            verifyToken();
            $data = json_decode(file_get_contents("php://input"), true);
            if (!isset($data['Nombre'], $data['Link'], $data['Imagen'], $data['Costo'], $data['Descripcion'])) {
                echo json_encode(["error" => "Faltan datos para crear el objeto."]);
                return;
            }

            try {
                $pdo->beginTransaction();

                // Insertar Objeto
                $stmt = $pdo->prepare("INSERT INTO objetos (Nombre, Link) VALUES (?, ?)");
                $stmt->execute([$data['Nombre'], $data['Link']]);
                $id_item = $pdo->lastInsertId();

                // Insertar Descripción del Objeto
                $stmt = $pdo->prepare("INSERT INTO objetos_descripcion (id_item, Nombre, Imagen, Costo, Descripcion) VALUES (?, ?, ?, ?, ?)");
                $stmt->execute([$id_item, $data['Nombre'], $data['Imagen'], $data['Costo'], $data['Descripcion']]);

                $pdo->commit();
                echo json_encode(["success" => "Objeto agregado", "id_item" => $id_item]);
            } catch (PDOException $e) {
                $pdo->rollBack();
                echo json_encode(["error" => "Error al agregar objeto", "message" => $e->getMessage()]);
            }
            break;

        case 'PUT': // Editar objeto y su descripción
            verifyToken();
            $data = json_decode(file_get_contents("php://input"), true);
            if (!isset($data['id'], $data['Nombre'], $data['Link'], $data['Imagen'], $data['Costo'], $data['Descripcion'])) {
                echo json_encode(["error" => "Faltan datos para actualizar el objeto."]);
                return;
            }

            try {
                $pdo->beginTransaction();

                // Actualizar Objeto
                $stmt = $pdo->prepare("UPDATE objetos SET Nombre = ?, Link = ? WHERE id_item = ?");
                $stmt->execute([$data['Nombre'], $data['Link'], $data['id']]);

                // Actualizar Descripción del Objeto
                $stmt = $pdo->prepare("UPDATE objetos_descripcion SET Nombre = ?, Imagen = ?, Costo = ?, Descripcion = ? WHERE id_item = ?");
                $stmt->execute([$data['Nombre'], $data['Imagen'], $data['Costo'], $data['Descripcion'], $data['id']]);

                $pdo->commit();
                echo json_encode(["success" => "Objeto actualizado"]);
            } catch (PDOException $e) {
                $pdo->rollBack();
                echo json_encode(["error" => "Error al actualizar objeto", "message" => $e->getMessage()]);
            }
            break;

        case 'DELETE': // Eliminar objeto y su descripción
            verifyToken();
            if (!$id) {
                echo json_encode(["error" => "ID de objeto requerido"]);
                return;
            }

            try {
                $pdo->beginTransaction();

                // Eliminar la descripción del objeto
                $stmt = $pdo->prepare("DELETE FROM objetos_descripcion WHERE id_item = ?");
                $stmt->execute([$id]);

                // Eliminar el objeto
                $stmt = $pdo->prepare("DELETE FROM objetos WHERE id_item = ?");
                $stmt->execute([$id]);

                $pdo->commit();
                echo json_encode(["success" => "Objeto eliminado"]);
            } catch (PDOException $e) {
                $pdo->rollBack();
                echo json_encode(["error" => "Error al eliminar objeto", "message" => $e->getMessage()]);
            }
            break;

        default:
            http_response_code(405);
            echo json_encode(["error" => "Método no permitido"]);
    }
}

