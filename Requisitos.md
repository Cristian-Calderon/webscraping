1. Configuracion de entorno de desarrollo.
- Tener instalado php, python y salenium.
- Configurar un servidor web local => apache

Para ver la version de php => php --version
Para ver la version de python => python3 --version
Para ver la version de selenium necesitamos instalar pip => pip3 --version


2. Crea la estructura basica del proyecto.
Crea las carpetas necesarias para organizar tu codigo:

src/
├── admin/
├── auth/
├── public/
├── scraping/
└── templates/

3. Crear un entorno virtual
Navegamos al directorio de tu proyecto

```bash
cd /var/www/webscraping.local
```

Creamos el entorno virtual
```bash
python3 -m venv entvirtual
```

Activar entorno virtual En linux/macOS
```bash
source entvirtual/bin/activate
```

Cuando el entorno esté activo, verás el nombre del entorno (env) al inicio de tu terminal, así:

```bash
(env) usuario@maquina:~/proyecto$
```

Instalar dependencias dentro del entorno

```bash
pip install selenium webdriver-manager
```

Driver google antes de instalar activar entorno virtual
```bash
pip install webdriver-manager
```

Instalar Selenium panda para guardar en csv
```bash
pip install selenium pandas
```

Ahora estas dependecias estaran aisladas para este proyecto

Ejecutar tu script dentro del entorno
```bash
python3 scraping_testpy
```

Desactivar el entorno virtual
```bash
deactivate
```

Ventajas de usar entornos virtuales
Aislamiento: Cada proyecto tiene sus propias dependencias.
Evitas conflictos: No se mezclan versiones de librerías entre proyectos.
Portabilidad: Puedes crear un archivo requirements.txt para replicar el entorno en otro sistema.

### Dependencias con git y entornos virtuales
Ignorar el entorno virtual creado, lo agregamos en el .gitignore
```bash
env/
```

Crear un archivo requirements.txt : Este archivo incluye todas las dependencias de tu proyecto con sus versiones. Puedes generarlo asi:
```bash
pip freeze > requirements.txt
```

## ¿Qué hago si cambio de ordenador o alguien clona mi proyecto?
Volvemos a crear un entorno
```bash
python3 -m venv env
```

Activamos el entorno
```bash
source env/bin/activate
```

Instala las dependencias desde el archivo requirements.txt
```bash
pip install -r requirements.txt
```


## Instalar composer 

Por terminal 
```bash
composer init
```

Requisitos :
Package name (<vendor>/<name>) cristiancalderon/webscraping
Description []: Webscraping

## Instalar Twig en componser
```bash
composer require twig/twig
```

## Instalacion de Librerias Firebase
```bash
composer requiere firebase/php-jwt
```

## Creacion de la base de datos
~~~sql
-- Crear la base de datos
CREATE DATABASE webscraping CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE webscraping;

-- Crear la tabla de usuarios
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Opcional: Crear la tabla de tokens revocados (para gestionar tokens JWT)
CREATE TABLE revoked_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token TEXT NOT NULL,
    revoked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
~~~

## Cambiar  virtual host
```bash
<VirtualHost *:80>
    ServerAdmin admin@webscraping.local
    ServerName www.webscraping.local
    ServerAlias webscraping.local
    DocumentRoot /var/www/webscraping.local/public
    <Directory> /var/www/webscraping.local/public >
        AllowOverride All
        Require all granted
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```



4. Implementa el scraping de datos:
- Crea un script en Python utilizando Selenium para extraer los datos de la web publica.
- Guardar los datos extraidos en un formato intermedio (CSV o XML)
- Insertar los datos en la base de datos del proyecto (base de datos)


ya intente de las maneras que me dijiste pero nada funciona, esta es la estructura de mi proyecto.

public  > templates > index.html.twig

<h1>Hola, {{ name }}!</h1>

<form action="../../src/auth/register.php" method="POST">

    <label for="username">Usuario:</label>
    <input type="text" id="username" name="username" required>
    
    <label for="email">Correo:</label>
    <input type="email" id="email" name="email" required>
    
    <label for="password">Contraseña:</label>
    <input type="password" id="password" name="password" required>
    
    <button type="submit">Registrarse</button>
</form>
        > index.php
        <?php

// require_once __DIR__ . '/vendor/autoload.php';
require_once "../vendor/autoload.php";
// require_once "../vendor/autoload.php";


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
        > test_db.php
        <?php
// require_once 'auth/config.php';
require_once '../src/auth/config.php';

if ($pdo) {
    echo "Conexión exitosa a la base de datos.";
} else {
    echo "Error al conectar.";
}


src > admin
    > auth  > login.php
            > config.php
            <?php
$host = 'localhost'; // Cambia si usas un host remoto
$db = 'webscraping';
$user = 'cris'; // Cambia al usuario configurado en MySQL
$password = '11011993'; // Añade la contraseña si tu usuario la tiene

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db;charset=utf8mb4", $user, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Error de conexión a la base de datos: " . $e->getMessage());
}

            > register.php
            <?php
// require_once 'config.php';
require_once './config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username']);
    $email = trim($_POST['email']);
    $password = trim($_POST['password']);

    // Validación básica
    if (empty($username) || empty($email) || empty($password)) {
        die('Todos los campos son obligatorios.');
    }

    // Verificar si el usuario ya existe
    $stmt = $pdo->prepare("SELECT * FROM users WHERE email = :email OR username = :username");
    $stmt->execute(['email' => $email, 'username' => $username]);
    if ($stmt->rowCount() > 0) {
        die('El usuario o correo ya están registrados.');
    }

    // Hashear la contraseña
    $hashedPassword = password_hash($password, PASSWORD_BCRYPT);

    // Insertar el usuario en la base de datos
    $stmt = $pdo->prepare("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)");
    if ($stmt->execute(['username' => $username, 'email' => $email, 'password' => $hashedPassword])) {
        echo 'Usuario registrado exitosamente.';
    } else {
        echo 'Error al registrar el usuario.';
    }
} else {
    die('Método no permitido.');
}

            > verify_token.php
    > scraping