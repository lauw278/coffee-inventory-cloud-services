import os
import logging
from flask import Flask, jsonify, request, render_template
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("coffee-inventory")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://coffee_app:coffee_app_password@db:5432/coffee_inventory"
)

def get_conn():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row, connect_timeout=3)

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id SERIAL PRIMARY KEY,
                name VARCHAR(120) NOT NULL,
                category VARCHAR(80) NOT NULL DEFAULT 'Coffee',
                quantity INTEGER NOT NULL CHECK (quantity >= 0),
                unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)
        conn.commit()

@app.before_request
def ensure_db_ready():
    # Schema creation is idempotent; if DB is not ready, return a clear error.
    try:
        init_db()
    except Exception:
        logger.exception("Database initialization/check failed")
        return jsonify({"error": "Database is unavailable. Check container status and logs."}), 503

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/health")
def health():
    try:
        with get_conn() as conn:
            conn.execute("SELECT 1")
        return jsonify({"status": "ok", "database": "connected"}), 200
    except Exception:
        logger.exception("Health check failed")
        return jsonify({"status": "error", "database": "unavailable"}), 503

@app.get("/api/items")
def list_items():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, name, category, quantity, unit_price, created_at FROM inventory ORDER BY id"
        ).fetchall()
    return jsonify([dict(row) for row in rows])

@app.post("/api/items")
def create_item():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    category = str(data.get("category", "Coffee")).strip() or "Coffee"
    quantity = data.get("quantity")
    unit_price = data.get("unit_price")

    if not name:
        return jsonify({"error": "Nama barang wajib diisi."}), 400
    if len(name) > 120 or len(category) > 80:
        return jsonify({"error": "Nama maksimal 120 karakter dan kategori maksimal 80 karakter."}), 400
    try:
        quantity = int(quantity)
        unit_price = float(unit_price)
    except (TypeError, ValueError):
        return jsonify({"error": "Stok harus bilangan bulat dan harga harus angka."}), 400
    if quantity < 0 or unit_price < 0:
        return jsonify({"error": "Stok dan harga tidak boleh negatif."}), 400

    with get_conn() as conn:
        row = conn.execute(
            "INSERT INTO inventory (name, category, quantity, unit_price) VALUES (%s, %s, %s, %s) "
            "RETURNING id, name, category, quantity, unit_price, created_at",
            (name, category, quantity, unit_price)
        ).fetchone()
        conn.commit()
    logger.info("Created inventory item id=%s", row["id"])
    return jsonify(dict(row)), 201

@app.put("/api/items/<int:item_id>")
def update_item(item_id):
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    category = str(data.get("category", "Coffee")).strip() or "Coffee"
    try:
        quantity = int(data.get("quantity"))
        unit_price = float(data.get("unit_price"))
    except (TypeError, ValueError):
        return jsonify({"error": "Stok harus bilangan bulat dan harga harus angka."}), 400
    if not name:
        return jsonify({"error": "Nama barang wajib diisi."}), 400
    if len(name) > 120 or len(category) > 80:
        return jsonify({"error": "Nama maksimal 120 karakter dan kategori maksimal 80 karakter."}), 400
    if quantity < 0 or unit_price < 0:
        return jsonify({"error": "Stok dan harga tidak boleh negatif."}), 400

    with get_conn() as conn:
        row = conn.execute(
            "UPDATE inventory SET name=%s, category=%s, quantity=%s, unit_price=%s "
            "WHERE id=%s RETURNING id, name, category, quantity, unit_price, created_at",
            (name, category, quantity, unit_price, item_id)
        ).fetchone()
        conn.commit()
    if row is None:
        return jsonify({"error": "Barang tidak ditemukan."}), 404
    logger.info("Updated inventory item id=%s", item_id)
    return jsonify(dict(row))

@app.delete("/api/items/<int:item_id>")
def delete_item(item_id):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM inventory WHERE id=%s", (item_id,))
        conn.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "Barang tidak ditemukan."}), 404
    logger.info("Deleted inventory item id=%s", item_id)
    return jsonify({"message": "Barang berhasil dihapus."})

if __name__ == "__main__":
    # Docker Compose waits for PostgreSQL healthcheck, then starts this service.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
