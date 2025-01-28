<?php
// require_once 'auth/config.php';
require_once '../src/auth/config.php';

if ($pdo) {
    echo "Conexión exitosa a la base de datos.";
} else {
    echo "Error al conectar.";
}



