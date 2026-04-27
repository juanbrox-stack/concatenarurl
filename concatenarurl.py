import streamlit as st
import pandas as pd
import io

# Configuración de la interfaz
st.set_page_config(page_title="Procesador Excel PrestaShop", layout="wide")

st.title("📦 Extractor de URLs para PrestaShop")
st.write("Sube tu Excel original y obtén uno nuevo con las URLs listas para importar.")

# Selector de archivos en el lateral
archivo = st.sidebar.file_uploader("Sube tu archivo Excel (.xlsx)", type=["xlsx"])

if archivo is not None:
    try:
        # 1. Leer el archivo Excel
        df = pd.read_excel(archivo)
        st.success("✅ Archivo cargado con éxito")

        # 2. Función lógica para limpiar y concatenar
        def procesar_urls(row):
            # Extrae celdas que son texto y empiezan por http
            urls = [str(val).strip() for val in row if pd.notna(val) and str(val).strip().lower().startswith('http')]
            # Une las primeras 10 con una coma
            return ','.join(urls[:10])

        # 3. Procesamiento (Mantenemos la primera columna como Referencia)
        ref_col = df.columns[0] 
        columnas_datos = df.columns[1:]
        
        resultado_df = pd.DataFrame()
        resultado_df[ref_col] = df[ref_col]
        resultado_df['Imágenes (Concatenadas)'] = df[columnas_datos].apply(procesar_urls, axis=1)

        # 4. Visualización
        st.subheader("Vista previa del resultado")
        st.dataframe(resultado_df.head(10), use_container_width=True)

        # 5. Generar botón de descarga (Excel)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            resultado_df.to_excel(writer, index=False, sheet_name='Prestashop')
        
        st.download_button(
            label="📥 Descargar Excel para PrestaShop",
            data=buffer.getvalue(),
            file_name="resultado_prestashop.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Hubo un error al leer el Excel: {e}")
else:
    st.info("👋 Por favor, sube un archivo .xlsx para procesar las URLs.")