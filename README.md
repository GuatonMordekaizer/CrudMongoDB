# ComercioTech DB

Backend de gestión de clientes, productos y pedidos para ComercioTech, construido con Flask, MongoDB y Docker.

---

## 📦 Características

- **CRUD Web** de clientes, productos y pedidos con Flask + Jinja2  
- **MongoDB** como almacén de datos  
- Despliegue reproducible con **Docker & Docker Compose**  
- **Tests** automatizados con pytest  
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
    ├── ExternalTest.py
    └── test_dummy.py
