import streamlit as st
from PyPDF2 import PdfReader

# --- CONFIGURACIÓN DE PRECIOS ---
COSTO_HOJA = 60
MARGEN = 1.40
PRECIO_ANILLADO = 2500 
ALIAS_PAGO = "tu.alias.aqui"

st.set_page_config(page_title="Gestor de Impresiones", page_icon="💰")

st.title("📑 Sistema de Pedidos")

archivo = st.file_uploader("Subí el PDF", type=["pdf"])

if archivo:
    reader = PdfReader(archivo)
    cant_paginas = len(reader.pages)
    
    col1, col2 = st.columns(2)
    with col1:
        doble_faz = st.checkbox("¿Doble Faz?", value=True)
    with col2:
        anillado = st.checkbox("¿Anillado?", value=False)

    # Lógica de costos
    hojas_fisicas = (cant_paginas + 1) // 2 if doble_faz else cant_paginas
    precio_hoja = COSTO_HOJA * MARGEN
    total_final = (hojas_fisicas * precio_hoja) + (PRECIO_ANILLADO if anillado else 0)
    
    adelanto = total_final / 2
    saldo = total_final - adelanto

    st.divider()
    
    # --- SELECCIÓN DE MÉTODO DE PAGO ---
    metodo_pago = st.selectbox("¿Cómo paga el anticipo?", ["Efectivo", "Transferencia"])

    st.subheader(f"Total: ${total_final:,.0f}")
    st.write(f"💵 **Anticipo a cobrar hoy:** ${adelanto:,.0f}")

    if metodo_pago == "Transferencia":
        st.info(f"Pedir comprobante a: **{ALIAS_PAGO}**")
    else:
        st.success("✅ Cobrar el efectivo en mano antes de confirmar.")

    nombre_cliente = st.text_input("Nombre del compañero")

    if st.button("Generar Orden"):
        if nombre_cliente:
            mensaje = (
                f"📝 *ORDEN DE IMPRESIÓN*%0A"
                f"--------------------------%0A"
                f"👤 *Cliente:* {nombre_cliente}%0A"
                f"💰 *TOTAL:* ${total_final:,.0f}%0A"
                f"💵 *ANTICIPO ({metodo_pago}):* ${adelanto:,.0f}%0A"
                f"📉 *SALDO PENDIENTE:* ${saldo:,.0f}%0A"
                f"--------------------------%0A"
                f"📄 {archivo.name} ({cant_paginas} págs)%0A"
            )
            
            wa_url = f"https://wa.me/549XXXXXXXXXX?text={mensaje}"
            st.markdown(f'[Confirmar y enviar por WhatsApp]({wa_url})')