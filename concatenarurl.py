import streamlit as st
import pandas as pd
import io

# Configuración de la página
st.set_page_config(page_title="Procesador de URLs Completo", layout="wide")

st.title("📦 Extractor de URLs para PrestaShop (Versión Completa)")
st.write("Esta versión asegura que las URLs no se corten al descargar el archivo.")

archivo = st.sidebar.file_uploader("Sube tu archivo Excel (.xlsx)", type=["xlsx"])

if archivo is not None:
    try:
        # Leer Excel original
        df = pd.read_excel(archivo)
        st.success("✅ Archivo cargado")

        # Función de procesamiento (Máximo 10 URLs, sin truncar)
        def procesar_urls(row):
            # Extraemos valores, limpiamos espacios y filtramos solo URLs válidas
            urls = [str(val).strip() for val in row if pd.notna(val) and str(val).strip().lower().startswith('http')]
            # Tomamos las 10 primeras y las unimos con coma (SIN espacios adicionales)
            return ','.join(urls[:10])

        # Asumimos Reference en la col 0
        ref_col = df.columns[0]
        columnas_urls = df.columns[1:]
        
        # Crear DataFrame de salida
        resultado_df = pd.DataFrame()
        resultado_df[ref_col] = df[ref_col].astype(str) # Asegurar que la referencia sea texto
        resultado_df['Imágenes (Concatenadas)'] = df[columnas_urls].apply(procesar_urls, axis=1)

        # Visualización para comprobar que el visual es correcto
        st.subheader("Confirmación visual (Primeras 10 filas)")
        st.dataframe(resultado_df.head(10), use_container_width=True)

        # --- MEJORA EN LA DESCARGA ---
        # Usamos un CSV con delimitador punto y coma y codificación utf-8-sig 
        # para que Excel lo abra perfecto y no trunque textos largos.
        csv_buffer = resultado_df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')

        # También ofrecemos la opción Excel directamente
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            resultado_df.to_excel(writer, index=False, sheet_name='Prestashop')
            # Ajuste automático del ancho de columna en el Excel generado
            worksheet = writer.sheets['Prestashop']
            worksheet.set_column('B:B', 100) # Darle mucho ancho a la columna de URLs

        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📊 Descargar como EXCEL (.xlsx)",
                data=excel_buffer.getvalue(),
                file_name="urls_completas_prestashop.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col2:
            st.download_button(
                label="📄 Descargar como CSV (Punto y coma)",
                data=csv_buffer,
                file_name="urls_completas_prestashop.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Sube un archivo Excel para procesar.")