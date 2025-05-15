# ComercioTech DB

Backend de gestión de clientes, productos y pedidos para ComercioTech, construido con Flask, MongoDB y Docker.

---

## 📦 Características

- **CRUD Web** de clientes, productos y pedidos con Flask + Jinja2  
- **MongoDB** como almacén de datos  
- Despliegue reproducible con **Docker & Docker Compose**  
- **Tests** automatizados con pytest (sin interfaz gráfica)  
- Front-end minimalista con HTML/CSS/JavaScript en `src/static` y plantillas en `src/templates`

---

## 📁 Estructura del proyecto

```text
comercitech-db/
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
└── src/
    ├── main.py
    ├── static/
    │   ├── css/style.css
    │   └── js/script.js
    └── templates/
        ├── base.html
        ├── clientes.html
        ├── cliente_detail.html
        ├── cliente_form.html
        ├── productos.html
        ├── producto_detail.html
        ├── producto_form.html
        ├── pedidos.html
        └── pedido_form.html
└── tests/
    ├── test_crud.py      # Pruebas desde consola sin GUI
    └── ExternalTest.py
```



## ⚙️ Prerrequisitos

- [Docker](https://www.docker.com/) ≥ 24.0  
- [Docker Compose](https://docs.docker.com/compose/) (incluido en Docker CLI)  
- (Opcional) Python ≥ 3.9 y `pip` para correr localmente


## 🔧 Variables de entorno

Crea un archivo `.env` en la raíz con estos valores:

```dotenv
MONGO_DB=comercitech
MONGO_USER=admin
MONGO_PASS=AdminP@ssw0rd!
MONGO_HOST=mongo
MONGO_PORT=27017
FLASK_ENV=development
```

---

## 🚀 Inicio rápido

1. **Levantar contenedores**  
   ```bash
   docker-compose up --build -d
   ```

2. **Abrir la aplicación**  
   En tu navegador, ve a:  
   ```
   http://localhost:5000
   ```

3. **Ejecutar pruebas desde consola**  
   Dentro del contenedor `app` o en tu entorno local con MongoDB corriendo:  
   ```bash
   pytest tests/test_crud.py --maxfail=1 --disable-warnings -q
   ```

4. **Detener y limpiar**  
   ```bash
   docker-compose down
   ```

---

## 🖥️ Uso de la aplicación

- **/clientes** — Lista, crea, edita y borra clientes  
- **/productos** — Lista, crea, edita y borra productos  
- **/pedidos** — Lista y gestiona pedidos  
- En formularios **Nuevo**, rellena campos y pulsa **Guardar**  
- Utiliza el buscador para filtrar resultados en listados  

---

## 📚 Recursos y referencias

- [Flask](https://flask.palletsprojects.com/)  
- [PyMongo](https://pymongo.readthedocs.io/)  
- [MongoDB Docker Image](https://hub.docker.com/_/mongo)  
- [Docker Compose reference](https://docs.docker.com/compose/compose-file/)  

---

## 📄 Licencia

Este proyecto está bajo la **MIT License**.  
