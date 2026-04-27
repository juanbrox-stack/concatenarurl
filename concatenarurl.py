import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="PrestaShop URL Merger", layout="wide")

st.title("🔗 Procesador Universal de Productos PrestaShop")
st.markdown("""
Esta herramienta cruza los datos de imágenes con la ficha de producto de PrestaShop.
1. **Primero** procesa las URLs (máximo 10).
2. **Después** busca el nombre y SKU en el fichero de productos para generar el archivo final.
""")

# --- SECCIÓN DE CARGA ---
col1, col2 = st.columns(2)

with col1:
    fichero_urls = st.file_uploader("1. Sube el Excel con las URLs", type=["xlsx", "csv"], key="urls")
with col2:
    fichero_prod = st.file_uploader("2. Sube el Excel de Productos (Estructura PrestaShop)", type=["xlsx", "csv"], key="prod")

if fichero_urls and fichero_prod:
    try:
        # Leer archivos
        df_urls_raw = pd.read_excel(fichero_urls) if "xlsx" in fichero_urls.name else pd.read_csv(fichero_urls)
        df_prod_raw = pd.read_excel(fichero_prod) if "xlsx" in fichero_prod.name else pd.read_csv(fichero_prod)

        # --- 1. PROCESAR URLS ---
        def limpiar_y_concatenar(row):
            # Filtra celdas que contienen http
            urls = [str(val).strip() for val in row if pd.notna(val) and "http" in str(val).lower()]
            return ",".join(urls[:10])

        # Creamos tabla de referencia: [SKU, URLs]
        ref_col_name = df_urls_raw.columns[0]
        df_fotos = pd.DataFrame()
        df_fotos['Reference'] = df_urls_raw[ref_col_name].astype(str).str.strip()
        df_fotos['urls_final'] = df_urls_raw.iloc[:, 1:].apply(limpiar_y_concatenar, axis=1)

        # --- 2. PROCESAR PRODUCTOS (Basado en posiciones fijas) ---
        # Columna C es índice 2 (Name)
        # Columna M es índice 12 (Reference #)
        df_info = pd.DataFrame()
        df_info['Name'] = df_prod_raw.iloc[:, 2] 
        df_info['Reference'] = df_prod_raw.iloc[:, 12].astype(str).str.strip()

        # --- 3. CRUCE DE DATOS (MERGE) ---
        resultado = pd.merge(df_info, df_fotos, on='Reference', how='left')

        # --- 4. ESTRUCTURA FINAL REQUERIDA ---
        # A: Reference, B: Name, C: URLs, D: Borrar con valor 0
        final_df = pd.DataFrame({
            'Reference': resultado['Reference'],
            'Name': resultado['Name'],
            'Image URLs (x,y,z...)': resultado['urls_final'],
            'Delete existing images (0 = No, 1 = Yes)': 0
        })

        st.success(f"✅ Se han cruzado {len(final_df)} productos correctamente.")

        # --- 5. VISUALIZACIÓN Y DESCARGA ---
        st.subheader("Vista previa del fichero resultante")
        st.dataframe(final_df.head(10), use_container_width=True)

        # Generar CSV para descarga
        # Usamos utf-8-sig para que Excel lo abra con tildes y caracteres especiales correctamente
        csv_buffer = final_df.to_csv(index=False, sep=';', encoding='utf-8-sig')
        
        st.download_button(
            label="📥 Descargar CSV para Importar en PrestaShop",
            data=csv_buffer,
            file_name="importacion_prestashop_final.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error al procesar: {e}. Comprueba que los archivos tienen las columnas en el orden correcto.")
else:
    st.info("Esperando la subida de ambos archivos...")