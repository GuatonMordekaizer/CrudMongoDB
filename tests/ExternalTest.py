import os
import logging
import platform
from typing import List, Dict
from urllib.parse import quote_plus
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId

# ===================== CONFIG =====================
DB_NAME = os.getenv("MONGO_DB", "comercitech")
USER = quote_plus(os.getenv("MONGO_USER", "admin"))
PASS = quote_plus(os.getenv("MONGO_PASS", "AdminP@ssw0rd!"))
HOST = os.getenv("MONGO_HOST", "localhost")
PORT = os.getenv("MONGO_PORT", "27017")

# ===================== LÍNEA DE MENU =====================
MENU_BORDER = "=" * 40

# --------------------- Funciones Utiles ---------------------
def clear_screen():
    cmd = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(cmd)

# --------------------- Logging ---------------------
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )

# --------------------- Conexion DB ---------------------
def get_db():
    uri = f"mongodb://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}?authSource=admin"
    logging.info(f"Conectando a MongoDB en {HOST}:{PORT}, db={DB_NAME}")
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    logging.info("Conexión OK")
    return client[DB_NAME]

# Inicialización global
configure_logging()
db = get_db()

# ===================== CRUD CLIENTES =====================
def crear_cliente():
    print(MENU_BORDER)
    print("Crear Cliente")
    print(MENU_BORDER)
    nombre = input("Nombre: ").strip()
    email = input("Email: ").strip()
    try:
        result = db.clientes.insert_one({"nombre": nombre, "email": email})
        print(f"-> Cliente creado con ID: {result.inserted_id}")
    except PyMongoError as e:
        print(f"Error: {e}")
    input("Presiona Enter para continuar...")

def listar_clientes():
    print(MENU_BORDER)
    print("Listado de Clientes")
    print(MENU_BORDER)
    for c in db.clientes.find():
        print(f"- {c['_id']}: {c['nombre']} <{c['email']}>")
    input("Presiona Enter para continuar...")

def buscar_cliente():
    print(MENU_BORDER)
    print("Buscar Cliente")
    print(MENU_BORDER)
    term = input("Email o Nombre: ").strip()
    results = list(db.clientes.find({"$or": [{"email": term}, {"nombre": term}]}))
    if results:
        for c in results:
            print(f"- {c['_id']}: {c['nombre']} <{c['email']}>")
    else:
        print("No se encontró cliente.")
    input("Presiona Enter para continuar...")

def actualizar_cliente():
    print(MENU_BORDER)
    print("Actualizar Cliente")
    print(MENU_BORDER)
    cid = input("ID Cliente: ").strip()
    campo = input("Campo (nombre/email): ").strip()
    valor = input("Nuevo Valor: ").strip()
    try:
        result = db.clientes.update_one({"_id": ObjectId(cid)}, {"$set": {campo: valor}})
        print(f"-> Documentos modificados: {result.modified_count}")
    except Exception as e:
        print(f"Error: {e}")
    input("Presiona Enter para continuar...")

def eliminar_cliente():
    print(MENU_BORDER)
    print("Eliminar Cliente")
    print(MENU_BORDER)
    cid = input("ID Cliente: ").strip()
    try:
        result = db.clientes.delete_one({"_id": ObjectId(cid)})
        print(f"-> Documentos eliminados: {result.deleted_count}")
    except Exception as e:
        print(f"Error: {e}")
    input("Presiona Enter para continuar...")

# ===================== CRUD PRODUCTOS =====================
def crear_producto():
    print(MENU_BORDER)
    print("Crear Producto")
    print(MENU_BORDER)
    sku = input("SKU: ").strip()
    nombre = input("Nombre: ").strip()
    categoria = input("Categoria: ").strip()
    precio = input("Precio: ").strip()
    try:
        precio = float(precio)
        result = db.productos.insert_one({"sku": sku, "nombre": nombre, "categoria": categoria, "precio": precio})
        print(f"-> Producto creado: {result.inserted_id}")
    except ValueError:
        print("Precio inválido.")
    except PyMongoError as e:
        print(f"Error: {e}")
    input("Presiona Enter para continuar...")

def listar_productos():
    print(MENU_BORDER)
    print("Listado de Productos")
    print(MENU_BORDER)
    for p in db.productos.find():
        print(f"- {p['_id']}: {p['sku']} - {p['nombre']} (${p['precio']})")
    input("Presiona Enter para continuar...")

def buscar_producto():
    print(MENU_BORDER)
    print("Buscar Producto")
    print(MENU_BORDER)
    term = input("SKU o Nombre: ").strip()
    results = list(db.productos.find({"$or": [{"sku": term}, {"nombre": term}]}))
    if results:
        for p in results:
            print(f"- {p['_id']}: {p['sku']} - {p['nombre']} (${p['precio']})")
    else:
        print("No se encontró producto.")
    input("Presiona Enter para continuar...")

def actualizar_producto():
    print(MENU_BORDER)
    print("Actualizar Producto")
    print(MENU_BORDER)
    sku = input("SKU: ").strip()
    campo = input("Campo (nombre/categoria/precio): ").strip()
    valor = input("Nuevo Valor: ").strip()
    try:
        if campo == "precio": valor = float(valor)
        result = db.productos.update_one({"sku": sku}, {"$set": {campo: valor}})
        print(f"-> Modificados: {result.modified_count}")
    except Exception as e:
        print(f"Error: {e}")
    input("Presiona Enter para continuar...")

def eliminar_producto():
    print(MENU_BORDER)
    print("Eliminar Producto")
    print(MENU_BORDER)
    sku = input("SKU: ").strip()
    try:
        result = db.productos.delete_one({"sku": sku})
        print(f"-> Eliminados: {result.deleted_count}")
    except Exception as e:
        print(f"Error: {e}")
    input("Presiona Enter para continuar...")

# ===================== CRUD PEDIDOS =====================
def crear_pedido():
    print(MENU_BORDER)
    print("Crear Pedido")
    print(MENU_BORDER)
    cid = input("ID Cliente: ").strip()
    items = input("Items (sku:cantidad, ...): ").strip()
    item_list: List[Dict] = []
    for pair in items.split(','):
        parts = pair.split(':')
        if len(parts) != 2:
            print(f"Formato inválido en '{pair}', se omite.")
            continue
        sku, qty = parts[0].strip(), parts[1].strip()
        try:
            item_list.append({"sku": sku, "cantidad": int(qty)})
        except ValueError:
            print(f"Cantidad inválida para SKU '{sku}', se omite.")
    if not item_list:
        print("No se añadieron items válidos.")
    else:
        try:
            result = db.pedidos.insert_one({"cliente_id": ObjectId(cid), "items": item_list})
            print(f"-> Pedido creado: {result.inserted_id}")
        except Exception as e:
            print(f"Error: {e}")
    input("Presiona Enter para continuar...")

def listar_pedidos():
    print(MENU_BORDER)
    print("Listado de Pedidos")
    print(MENU_BORDER)
    for o in db.pedidos.find():
        print(f"- {o['_id']}: Cliente {o['cliente_id']} Items {o['items']}")
    input("Presiona Enter para continuar...")

def buscar_pedido():
    print(MENU_BORDER)
    print("Buscar Pedido")
    print(MENU_BORDER)
    pid = input("ID Pedido: ").strip()
    try:
        doc = db.pedidos.find_one({"_id": ObjectId(pid)})
        print(doc or "No encontrado")
    except Exception as e:
        print(f"Error: {e}")
    input("Presiona Enter para continuar...")

def actualizar_pedido():
    print(MENU_BORDER)
    print("Actualizar Pedido")
    print(MENU_BORDER)
    pid = input("ID Pedido: ").strip()
    campo = input("Campo (e.g., estado): ").strip()
    valor = input("Nuevo Valor: ").strip()
    try:
        result = db.pedidos.update_one({"_id": ObjectId(pid)}, {"$set": {campo: valor}})
        print(f"-> Modificados: {result.modified_count}")
    except Exception as e:
        print(f"Error: {e}")
    input("Presiona Enter para continuar...")

def eliminar_pedido():
    print(MENU_BORDER)
    print("Eliminar Pedido")
    print(MENU_BORDER)
    pid = input("ID Pedido: ").strip()
    try:
        result = db.pedidos.delete_one({"_id": ObjectId(pid)})
        print(f"-> Eliminados: {result.deleted_count}")
    except Exception as e:
        print(f"Error: {e}")
    input("Presiona Enter para continuar...")

# ===================== MENU PRINCIPAL =====================
def main_menu():
    options = [
        "1) Clientes: Crear, Listar, Buscar, Actualizar, Eliminar",
        "2) Productos: Crear, Listar, Buscar, Actualizar, Eliminar",
        "3) Pedidos: Crear, Listar, Buscar, Actualizar, Eliminar",
        "0) Salir"
    ]
    while True:
        clear_screen()
        print(MENU_BORDER)
        print("    CRUD ComercioTech - Menú Principal")
        print(MENU_BORDER)
        for opt in options:
            print(opt)
        choice = input("Selecciona sección: ").strip()
        if choice == '0':
            print("Saliendo...")
            break
        elif choice == '1':
            submenu([crear_cliente, listar_clientes, buscar_cliente, actualizar_cliente, eliminar_cliente], "Clientes")
        elif choice == '2':
            submenu([crear_producto, listar_productos, buscar_producto, actualizar_producto, eliminar_producto], "Productos")
        elif choice == '3':
            submenu([crear_pedido, listar_pedidos, buscar_pedido, actualizar_pedido, eliminar_pedido], "Pedidos")
        else:
            input("Opción inválida. Presiona Enter...")

# Submenu genérico
def submenu(actions: List, title: str):
    while True:
        clear_screen()
        print(MENU_BORDER)
        print(f"   {title} - Opciones")
        print(MENU_BORDER)
        for idx, func in enumerate(actions, 1):
            print(f"{idx}) {func.__name__.replace('_', ' ').title()}")
        print("0) Volver")
        choice = input("Elige opción: ").strip()
        if choice == '0': break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(actions):
                actions[idx]()
            else:
                input("Índice fuera de rango. Enter...")
        except ValueError:
            input("Entrada inválida. Enter...")

if __name__ == "__main__":
    main_menu()
# EOF