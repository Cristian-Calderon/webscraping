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


4. Implementa el scraping de datos:
- Crea un script en Python utilizando Selenium para extraer los datos de la web publica.
- Guardar los datos extraidos en un formato intermedio (CSV o XML)
- Insertar los datos en la base de datos del proyecto (base de datos)
