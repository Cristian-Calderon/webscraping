<?php
// Eliminar la cookie del token
setcookie("auth_token", "", time() - 3600, "/");

// Redirigir al login
header("Location: /login");
exit();
