import streamlit as st
from PyPDF2 import PdfReader

# --- CONFIGURACIÓN DE PRECIOS ---
COSTO_HOJA_BASE = 60
MARGEN_GANANCIA = 1.40  # 40%
PRECIO_ANILLADO = 2500  # Ajustalo según tu costo
ALIAS_MP = "mgr.salta.mp" # Reemplazar con el tuyo

st.set_page_config(page_title="Calculadora de Impresiones", page_icon="📝")

st.title("🖨️ Gestor de Pedidos")
st.write("Calculá presupuestos y gestioná el cobro de anticipos.")

# Subida de archivo
archivo = st.file_uploader("Subí el PDF del compañero", type=["pdf"])

if archivo:
    # Leer PDF
    pdf = PdfReader(archivo)
    cant_paginas = len(pdf.pages)
    
    st.info(f"El archivo tiene **{cant_paginas}** páginas.")

    # Opciones de impresión
    col1, col2 = st.columns(2)
    with col1:
        doble_faz = st.checkbox("Impresión Doble Faz", value=True)
    with col2:
        anillado = st.checkbox("¿Lleva Anillado?", value=False)

    # Cálculos
    hojas_fisicas = (cant_paginas + 1) // 2 if doble_faz else cant_paginas
    precio_unidad = COSTO_HOJA_BASE * MARGEN_GANANCIA
    
    total_impresion = hojas_fisicas * precio_unidad
    total_final = total_impresion + (PRECIO_ANILLADO if anillado else 0)
    
    adelanto_minimo = total_final / 2
    saldo_restante = total_final - adelanto_minimo

    # --- MOSTRAR RESUMEN VISUALMENTE IMPACTANTE ---
    st.divider()
    st.subheader("💰 Resumen del Presupuesto")

    # Cuadro destacado con el Total Final
    st.markdown(
        f"""
        <div style="
            background-color: #d4edda; 
            padding: 20px; 
            border-radius: 10px; 
            border: 2px solid #28a745;
            text-align: center;
            margin-bottom: 20px;">
            <h2 style="color: #155724; margin: 0; font-size: 1.2em;">TOTAL FINAL</h2>
            <h1 style="color: #155724; margin: 0; font-size: 3em;">${total_final:,.0f}</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Detalles del adelanto y saldo en columnas
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**💵 Anticipo (50%):**")
        st.subheader(f"${adelanto_minimo:,.0f}")
    with c2:
        st.write(f"**📉 Saldo al recibir:**")
        st.subheader(f"${saldo_restante:,.0f}")

    # Gestión de Pago
    metodo = st.radio("¿Cómo paga el anticipo?", ["Efectivo", "Transferencia"])
    
    if metodo == "Transferencia":
        st.warning(f"Alias para el pago: **{ALIAS_MP}**")
    
    nombre_compañero = st.text_input("Nombre del compañero/profe")

    if st.button("✅ Generar Orden y Enviar WhatsApp"):
        if nombre_compañero:
            # Crear mensaje para WhatsApp
            msg = (
                f"📝 *NUEVA ORDEN DE IMPRESIÓN*%0A"
                f"--------------------------%0A"
                f"👤 *Cliente:* {nombre_compañero}%0A"
                f"📄 *Archivo:* {archivo.name}%0A"
                f"📑 *Páginas:* {cant_paginas}%0A"
                f"🔄 *Formato:* {'Doble faz' if doble_faz else 'Simple faz'}%0A"
                f"🌀 *Anillado:* {'Si' if anillado else 'No'}%0A"
                f"--------------------------%0A"
                f"💰 *TOTAL:* ${total_final:,.0f}%0A"
                f"💵 *ANTICIPO ({metodo}):* ${adelanto_minimo:,.0f}%0A"
                f"📉 *SALDO PENDIENTE:* ${saldo_restante:,.0f}%0A"
                f"--------------------------%0A"
                f"🚀 _Pedido confirmado. ¡Gracias!_"
            )
            
            # Aquí va el número de tu hijo o el tuyo
            whatsapp_url = f"https://wa.me/5493874404730?text={msg}"
            
            st.markdown(f'<a href="{whatsapp_url}" target="_blank">Abrir WhatsApp para enviar orden</a>', unsafe_allow_html=True)
        else:
            st.error("Por favor, poné el nombre de quién hace el pedido.")