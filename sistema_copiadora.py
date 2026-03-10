import streamlit as st
import sqlite3
from datetime import datetime

# -------- BASE DE DATOS --------

conn = sqlite3.connect("pedidos.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
id INTEGER PRIMARY KEY AUTOINCREMENT,
fecha TEXT,
empleado TEXT,
hojas INTEGER,
cantidad INTEGER,
tipo TEXT,
tapas INTEGER,
anillado INTEGER,
precio_unitario REAL,
total REAL
)
""")

conn.commit()

# -------- COSTOS --------

precio_resma = 5179
precio_tapas_pack = 5910
precio_anillos_pack = 2418

costo_copia_bn = 6
costo_copia_color = 35

costo_hoja = precio_resma / 500
costo_tapa = precio_tapas_pack / 50
costo_anillo = precio_anillos_pack / 50

# -------- INTERFAZ --------

st.title("Sistema de Copiadora")

empleado = st.text_input("Empleado")

hojas = st.number_input("Hojas por cartilla", 1, 500, 76)
cantidad = st.number_input("Cantidad", 1, 500, 1)

tipo = st.selectbox("Tipo impresión", ["Blanco y Negro","Color"])

tapas = st.checkbox("Tapas")
anillado = st.checkbox("Anillado")

# -------- CALCULO --------

copias = hojas * 2

costo_impresion = copias * (costo_copia_bn if tipo=="Blanco y Negro" else costo_copia_color)

costo_total = hojas * costo_hoja + costo_impresion

if tapas:
    costo_total += costo_tapa * 2

if anillado:
    costo_total += costo_anillo

precio_unitario = costo_total * 1.8
total = precio_unitario * cantidad

st.subheader("Resultado")

st.write("Costo unitario:", round(costo_total,2))
st.write("Precio unitario sugerido:", round(precio_unitario,2))
st.write("Total a cobrar:", round(total,2))

# -------- GUARDAR PEDIDO --------

if st.button("Guardar pedido"):

    cursor.execute("""
    INSERT INTO pedidos (
    fecha,empleado,hojas,cantidad,tipo,tapas,anillado,precio_unitario,total
    ) VALUES (?,?,?,?,?,?,?,?,?)
    """,(
    datetime.now().strftime("%Y-%m-%d %H:%M"),
    empleado,
    hojas,
    cantidad,
    tipo,
    int(tapas),
    int(anillado),
    precio_unitario,
    total
    ))

    conn.commit()

    st.success("Pedido guardado")

# -------- HISTORIAL --------

st.subheader("Pedidos recientes")

cursor.execute("SELECT * FROM pedidos ORDER BY id DESC LIMIT 20")
rows = cursor.fetchall()

for r in rows:
    st.write(r)