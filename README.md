# Proyecto: DotaStats

[![Screenshot-from-2025-03-17-22-22-58.png](https://i.postimg.cc/HxSxvmLD/Screenshot-from-2025-03-17-22-22-58.png)](https://postimg.cc/CBqSdWDm)

## Descripcion

Este proyecto es una aplicacion web desarrollada con php, twig y javascript para el front-end, utilizando mysql como base de datos y una API para la comunicacion entre el front y el back-end. La informacion scrapeada fue conseguida de la siguiente pagina web : https://www.dotabuff.com/

La pagina web se trata de estadisticas de heroes de un video juego llamado dota 2 donde se guardaron los heroes y las objetos de todo el juego.

Entre las funciones destacadas se encuentran:
- Graficas circulares de estadisticas como fuerza agilidad y inteligencia de cada heroe(personaje).
- Añadir, Heroe
- Añadir, editar o eliminar objetos.
- Permite registrarse en la aplicacion web
- Permite hacer un login.

## Tecnologias Utilizadas
- PHP  
- Twig
- MySQL
- API REST
- HTML, CSS, JavaScript
- Bootstrap
- Twig
- Selenium (con Python)
- JWT (JSON Web Tokens)
- Script Bash

# Creación de una página web dinámica en PHP

## Objetivo

El objetivo de esta práctica es el desarrollo de una página web dinámica en PHP que incluya una serie de funcionalidades avanzadas para gestionar, visualizar y editar datos de una fuente externa. Los datos se obtendrán mediante técnicas de web scraping usando `Selenium` con `Python`. El proyecto también requerirá la implementación de autenticación segura mediante tokens `JWT`, una interfaz de administración protegida, y la internacionalización para soportar múltiples idiomas.

## Especificaciones Técnicas

La práctica deberá cumplir con las siguientes especificaciones:

### Front-end con Bootstrap y TWIG

Implementa la interfaz de usuario utilizando el framework `Bootstrap` para asegurar un diseño responsive y moderno.
La página principal debe mostrar los datos scrapeados, con la posibilidad de que los usuarios puedan interactuar con ellos (ej., búsquedas, filtros, etc.).

Utilización del sistema de plantillas `TWIG` para la representación de los datos.

### Gráficas con alguna librería de JavaScript o mapas con GoogleMaps o OpenStreetMap

A partir de los datos extraídos podría ser interesante presentar la información con alguna librería gráfica, ya sea librerías como `D3.js`, `Chart.js`, `Highcharts`, etc. o representar información geolocalizada con `GoogleMaps` o `OpenStreetMap` o similares.

### Routing en PHP

Implementa un sistema de routing en `PHP` que permita gestionar las diferentes rutas de la aplicación (ej., página principal, página de administración, autenticación, etc.).
Cada ruta debe estar claramente separada para facilitar la mantenibilidad del código.

### Panel de Administración

Crea un panel de administración accesible solo para usuarios autenticados, desde donde se puedan gestionar los datos obtenidos a través de scraping.
Los datos que se scrapeen deben ser almacenados en una base de datos y ser editables desde este panel.

### Autenticación mediante API y JWT

Implementa una API autenticada mediante `JWT` (`JSON Web Tokens`) para manejar la autenticación de usuarios.
La autenticación debe permitir el inicio de sesión y la permanencia de la sesión incluso si el usuario cierra el navegador, utilizando cookies y sesiones.
La API debe proteger el acceso a las rutas y funcionalidades del panel de administración para asegurar que solo usuarios autenticados tengan acceso.

### Internacionalización
La aplicación debe soportar internacionalización utilizando la biblioteca `gettext` en `PHP`.
Implementa al menos dos idiomas (ej., español e inglés), y asegúrate de que todas las interfaces de usuario y mensajes estén traducidos correctamente.

### Scraping de Datos con Selenium y Python
Realiza el scraping de datos en una web pública utilizando `Selenium` en `Python`.
Los datos obtenidos deben ser estructurados y almacenados en una base de datos en el servidor del proyecto.
El script de scraping debe ser capaz de ejecutarse de manera independiente y almacenar los datos en la base de datos para luego ser gestionados desde el panel de administración.
Se recomienda que el script de scraping extraiga los datos y los guarde en un fomarto intermedio, por ejemplo, `CSV` o `XML`. Posteriormente debería recorrerse el archivo de datos extraídos e insertar los datos en nuestra base de datos.

### Modelo de Datos en Base de Datos
Crea un modelo de datos adecuado para almacenar la información scrapeada en la base de datos.
El modelo de datos debe ser estructurado de manera que permita futuras ampliaciones o cambios sin grandes modificaciones en el sistema.
El modelo de datos deberá contar al menos con tres clases (tablas) relacionadas entre ellas. 
Es necesario presentar el modelo de datos al profesor préviamente a la extracción de los mismos.

### Gestión de Sesiones y Cookies
Implementa la gestión de sesiones y cookies para mantener al usuario conectado en caso de que cierre el navegador, permitiendo el acceso continuo a la administración.

## Requerimientos de Entrega

* **Estructura del código**: El código debe estar estructurado y organizado en módulos claros y separados (routing, autenticación, scraping, etc.).
* **Comentarios y documentación**: Todo el código debe estar correctamente comentado y documentado para facilitar su comprensión y revisión.
* **Repositorio en GitHub**: El proyecto debe estar alojado en un repositorio privado de `GitHub` y compartido con el profesor para su evaluación.
* **README.md**: El proyecto debe incluir un archivo `README.md` que explique cómo instalar y ejecutar el proyecto, junto con una descripción general de la estructura del código y las tecnologías utilizadas.

## Evaluación y valoración

La evaluación de la práctica considerará los siguientes aspectos:

* **Funcionalidad completa**: Se valorará que la página cumpla con todas las funcionalidades requeridas (scraping, panel de administración, internacionalización, autenticación con JWT, etc.).
* **Diseño y usabilidad**: La interfaz de usuario debe ser intuitiva, clara y profesional, y ser completamente funcional en dispositivos móviles y de escritorio.
* **Estructura y calidad del código**: Se valorará la organización del código, la claridad en los comentarios y la estructura de los archivos.
* **Documentación completa**: La documentación debe estar bien escrita y ser suficiente para permitir a otro desarrollador comprender y ejecutar el proyecto fácilmente.

### Recomendaciones

* Asegúrate de probar el sistema de autenticación para verificar que protege adecuadamente las rutas sensibles.
* Realiza pruebas de la internacionalización para confirmar que las traducciones son correctas y que el cambio de idioma funciona en toda la aplicación.
* Realiza pruebas de carga en el scraping para optimizar el tiempo de ejecución y asegurar que se maneje cualquier posible cambio en la estructura de la página objetivo.


## Instalacion
1. Clonar el repositorio :
```bash
git clone https://github.com/Cristian-Calderon/webscraping.git
```
2. Acceder al directorio del proyecto
```bash
cd webscraping
```
3. Instalar las dependecias 
```bash
composer install
```
4. Configurar la base de datos:
- Crear una base de datos MySQL .
- Importar el archivo `database.sql`.

## Configuracion de VirtualHost

Configurar VirtualHost:
```bash
sudo vim /etc/apache2/sites-available/webscraping.local.conf
```
```bash
<VirtualHost *:80>
    ServerAdmin admin@webscraping.local
    ServerName www.webscraping.local
    ServerAlias webscraping.local
    DocumentRoot /var/www/webscraping.local/public
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
Podemos añadir la entrada en /etc/hosts
```bash
sudo nvim /etc/hosts
```
```bash
127.0.0.1  webscraping.local www.webscraping.local
```

##Pruebas
### Añadir heroe con un formulario:
[![Screenshot-from-2025-03-17-23-09-21.png](https://i.postimg.cc/0r1bDfQb/Screenshot-from-2025-03-17-23-09-21.png)](https://postimg.cc/T5QdXnn6)
Donde tendremos que agregar lo siguientes atributos:
1. Nombre del personaje,
2. La imagen que tiene que ser una url 
3. La popularidad
4. Porcentaje de victoria
5. Resultado que es [won, lost]
6. Fuerza
7. Agilidad
8. Inteligencia
9. Velocidad de movimiento
10. Rango de vision
11. Armadura
12. Tiempo de Ataque Base
13. Daño
14. Punto de Ataque

Tambien puede contar con habilidades :
1. Nombre de la habilidad
2. Descripcion de la habilidad
3. Link imagen de la habilidad


[![Screenshot-from-2025-03-17-23-15-57.png](https://i.postimg.cc/KY8Dsn71/Screenshot-from-2025-03-17-23-15-57.png)](https://postimg.cc/xXBmXN4Q)

### Añadir Objetos
[![Screenshot-from-2025-03-17-23-21-13.png](https://i.postimg.cc/bYkkgCX6/Screenshot-from-2025-03-17-23-21-13.png)](https://postimg.cc/kDM2Xyg8)

Para añadir objetos necesitamos:
1. Nombre del objeto
2. Url de la imagen
3. Costo
4. Descripcion

[![Screenshot-from-2025-03-17-23-22-07.png](https://i.postimg.cc/Kv5LS18B/Screenshot-from-2025-03-17-23-22-07.png)](https://postimg.cc/xccqLTH1)

### Editar Objetos

[![Screenshot-from-2025-03-17-23-22-53.png](https://i.postimg.cc/rwF48qDb/Screenshot-from-2025-03-17-23-22-53.png)](https://postimg.cc/vckThFLL)

### Eliminar Objetos
[![Screenshot-from-2025-03-17-23-23-23.png](https://i.postimg.cc/P53wJ0Zq/Screenshot-from-2025-03-17-23-23-23.png)](https://postimg.cc/4YcdFLWC)


## Autor
Cristian Calderon 

## Licencia 
Este proyecto esta bajo la licencia MIT