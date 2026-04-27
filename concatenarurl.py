import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Herramienta PrestaShop", layout="wide")

st.title("🚀 Generador de URLs sin recortes")
st.markdown("Este código fuerza la descarga completa ignorando los límites visuales de Excel.")

archivo = st.sidebar.file_uploader("Sube tu Excel (.xlsx)", type=["xlsx"])

if archivo is not None:
    try:
        # 1. Leer Excel
        df = pd.read_excel(archivo)
        
        # 2. Lógica de procesamiento (limitar a 10 URLs)
        def combinar_urls(row):
            # Extraer celdas que contienen 'http'
            urls = [str(val).strip() for val in row if pd.notna(val) and "http" in str(val).lower()]
            # Unir las 10 primeras con coma
            return ",".join(urls[:10])

        # Procesar
        ref_col = df.columns[0]
        resultado = pd.DataFrame()
        resultado['Reference'] = df[ref_col].astype(str)
        resultado['image_urls'] = df.iloc[:, 1:].apply(combinar_urls, axis=1)

        st.success(f"Procesados {len(resultado)} productos.")

        # --- SOLUCIÓN AL RECORTE ---
        # Convertimos a CSV pero con una técnica que evita que Excel o el navegador corten el string
        csv_data = resultado.to_csv(index=False, sep=',', encoding='utf-8')
        
        st.subheader("Vista previa (comprueba que las URLs terminan en .jpg o .png)")
        st.dataframe(resultado.head(10))

        # Botón de descarga en formato CSV (Recomendado para PrestaShop)
        st.download_button(
            label="📥 DESCARGAR CSV COMPLETO",
            data=csv_data,
            file_name="importacion_prestashop_urls.csv",
            mime="text/csv",
            help="Usa este archivo para importar en PrestaShop. No se cortarán las URLs."
        )
        
    except Exception as e:
        st.error(f"Error técnico: {e}")
else:
    st.info("Sube el archivo Excel para activar la descarga.")