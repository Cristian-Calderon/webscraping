🔹 Paso 1: Agregar un Campo role en la Base de Datos
📌 Primero, necesitamos diferenciar entre administradores y usuarios normales.
Ejecuta esta consulta SQL en tu base de datos para agregar el campo role:

```sql
ALTER TABLE users ADD COLUMN role ENUM('admin', 'user') NOT NULL DEFAULT 'user';
```

Para agregar administrador 

```sql
UPDATE users SET role = 'admin' WHERE email = 'tucorreo@admin.com';
```

