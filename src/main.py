import os
import logging
from urllib.parse import quote_plus
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson import ObjectId

# ===================== CONFIG =====================
DB_NAME = os.getenv("MONGO_DB", "comercitech")
USER = quote_plus(os.getenv("MONGO_USER", "admin"))
PASS = quote_plus(os.getenv("MONGO_PASS", "AdminP@ssw0rd!"))
HOST = os.getenv("MONGO_HOST", "mongo")
PORT = os.getenv("MONGO_PORT", "27017")

# ===================== LOGGING =====================
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ===================== DB CONNECTION =====================
uri = f"mongodb://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}?authSource=admin"
logger.info(f"Connecting to MongoDB: {uri}")
client = MongoClient(uri)
db = client[DB_NAME]

# ===================== FLASK APP =====================
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", "supersecret")

# --------------------- ROOT & ERROR HANDLERS ---------------------
@app.route('/')
def home():
    logger.debug("Redirecting to list_clientes")
    return redirect(url_for('list_clientes'))

@app.errorhandler(404)
def not_found(e):
    logger.warning(f"404 Error: {request.path}")
    return redirect(url_for('home'))

# ===================== CRUD CLIENTES =====================
@app.route('/clientes')
def list_clientes():
    q = request.args.get('q', '')
    logger.debug(f"Listing clientes with filter: {q}")
    filter_q = {'$regex': q, '$options': 'i'} if q else None
    query = {'$or': [{'nombre': filter_q}, {'email': filter_q}]} if q else {}
    clientes = list(db.clientes.find(query))
    return render_template('clientes.html', clientes=clientes, q=q)

@app.route('/clientes/nuevo', methods=['GET','POST'])
def new_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        logger.info(f"Creating cliente: {nombre}, {email}")
        db.clientes.insert_one({'nombre': nombre, 'email': email})
        flash('Cliente creado con éxito', 'success')
        return redirect(url_for('list_clientes'))
    return render_template('cliente_form.html', cliente=None)

@app.route('/clientes/<id>')
def detail_cliente(id):
    logger.debug(f"Detail cliente: {id}")
    c = db.clientes.find_one({'_id': ObjectId(id)})
    return render_template('cliente_detail.html', cliente=c)

@app.route('/clientes/<id>/editar', methods=['GET','POST'])
def edit_cliente(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        logger.info(f"Updating cliente {id} to {nombre}, {email}")
        db.clientes.update_one({'_id': ObjectId(id)}, {'$set': {'nombre': nombre, 'email': email}})
        flash('Cliente actualizado', 'info')
        return redirect(url_for('list_clientes'))
    c = db.clientes.find_one({'_id': ObjectId(id)})
    return render_template('cliente_form.html', cliente=c)

@app.route('/clientes/<id>/borrar', methods=['POST'])
def delete_cliente(id):
    logger.info(f"Deleting cliente: {id}")
    db.clientes.delete_one({'_id': ObjectId(id)})
    flash('Cliente eliminado', 'warning')
    return redirect(url_for('list_clientes'))

# ===================== CRUD PRODUCTOS =====================
@app.route('/productos')
def list_productos():
    q = request.args.get('q', '')
    logger.debug(f"Listing productos with filter: {q}")
    filter_q = {'$regex': q, '$options': 'i'} if q else None
    query = {'$or': [{'sku': filter_q}, {'nombre': filter_q}]} if q else {}
    productos = list(db.productos.find(query))
    return render_template('productos.html', productos=productos, q=q)

@app.route('/productos/nuevo', methods=['GET','POST'])
def new_producto():
    if request.method == 'POST':
        sku = request.form['sku']
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        logger.info(f"Creating producto: {sku}, {nombre}, {precio}")
        db.productos.insert_one({'sku': sku, 'nombre': nombre, 'precio': precio})
        flash('Producto creado', 'success')
        return redirect(url_for('list_productos'))
    return render_template('producto_form.html', producto=None)

@app.route('/productos/<id>')
def detail_producto(id):
    logger.debug(f"Detail producto: {id}")
    p = db.productos.find_one({'_id': ObjectId(id)})
    return render_template('producto_detail.html', producto=p)

@app.route('/productos/<id>/editar', methods=['GET','POST'])
def edit_producto(id):
    if request.method == 'POST':
        sku = request.form['sku']
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        logger.info(f"Updating producto {id}: {sku}, {nombre}, {precio}")
        db.productos.update_one({'_id': ObjectId(id)}, {'$set': {'sku': sku, 'nombre': nombre, 'precio': precio}})
        flash('Producto actualizado', 'info')
        return redirect(url_for('list_productos'))
    p = db.productos.find_one({'_id': ObjectId(id)})
    return render_template('producto_form.html', producto=p)

@app.route('/productos/<id>/borrar', methods=['POST'])
def delete_producto(id):
    logger.info(f"Deleting producto: {id}")
    db.productos.delete_one({'_id': ObjectId(id)})
    flash('Producto eliminado', 'warning')
    return redirect(url_for('list_productos'))

# ===================== CRUD PEDIDOS =====================
@app.route('/pedidos')
def list_pedidos():
    logger.debug("Listing pedidos")
    pedidos = list(db.pedidos.find())
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/pedidos/nuevo', methods=['GET','POST'])
def new_pedido():
    clientes = list(db.clientes.find())
    if request.method == 'POST':
        cid = request.form['cliente']
        raw_items = request.form.get('items', '')
        logger.info(f"Raw items input: {raw_items}")
        items = []
        for pair in raw_items.split(','):
            pair = pair.strip()
            if not pair:
                continue
            parts = pair.split(':')
            if len(parts) != 2:
                logger.error(f"Malformed item entry: '{pair}'")
                continue
            sku, qty_str = parts[0].strip(), parts[1].strip()
            try:
                qty = int(qty_str)
                items.append({'sku': sku, 'cantidad': qty})
                logger.debug(f"Parsed item: {sku} x {qty}")
            except ValueError:
                logger.error(f"Invalid quantity for item '{pair}'")
        logger.info(f"Creating pedido for cliente {cid} with items: {items}")
        db.pedidos.insert_one({'cliente_id': ObjectId(cid), 'items': items, 'estado': 'pendiente'})
        flash('Pedido creado', 'success')
        return redirect(url_for('list_pedidos'))
    return render_template('pedido_form.html', clientes=clientes, pedido=None)

@app.route('/pedidos/<id>')
def detail_pedido(id):
    logger.debug(f"Detail pedido: {id}")
    o = db.pedidos.find_one({'_id': ObjectId(id)})
    cliente = db.clientes.find_one({'_id': ObjectId(o['cliente_id'])})
    return render_template('pedido_detail.html', pedido=o, cliente=cliente)

@app.route('/pedidos/<id>/editar', methods=['GET','POST'])
def edit_pedido(id):
    o = db.pedidos.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        estado = request.form['estado']
        logger.info(f"Updating pedido {id} to estado {estado}")
        db.pedidos.update_one({'_id': ObjectId(id)}, {'$set': {'estado': estado}})
        flash('Pedido actualizado', 'info')
        return redirect(url_for('list_pedidos'))
    clientes = list(db.clientes.find())
    return render_template('pedido_form.html', clientes=clientes, pedido=o)

@app.route('/pedidos/<id>/borrar', methods=['POST'])
def delete_pedido(id):
    logger.info(f"Deleting pedido: {id}")
    db.pedidos.delete_one({'_id': ObjectId(id)})
    flash('Pedido eliminado', 'warning')
    return redirect(url_for('list_pedidos'))

# ===================== MAIN =====================
if __name__ == '__main__':
    logger.info("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000)
# EOF
