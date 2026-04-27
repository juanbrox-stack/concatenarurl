import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Mi App de Datos", layout="wide")

st.title("🚀 Analizador de Productos para PrestaShop")
st.markdown("""
Esta aplicación permite cargar ficheros CSV y visualizar las URLs de productos rápidamente.
""")

# Barra lateral para configuración
st.sidebar.header("Configuración")
archivo_subido = st.sidebar.file_uploader("Sube tu archivo CSV", type=["csv"])

if archivo_subido is not None:
    # Leer el archivo
    df = pd.read_csv(archivo_subido)
    
    # Mostrar métricas rápidas
    col1, col2 = st.columns(2)
    col1.metric("Total de Productos", len(df))
    col2.metric("Columnas detectadas", len(df.columns))

    # Buscador en el dataframe
    st.subheader("Vista previa de los datos")
    search = st.text_input("Filtrar por referencia o contenido:")
    
    if search:
        df_display = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    else:
        df_display = df

    st.dataframe(df_display, use_container_width=True)

    # Botón de descarga para el usuario
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar datos actuales",
        data=csv,
        file_name='datos_procesados.csv',
        mime='text/csv',
    )
else:
    st.info("💡 Por favor, sube un archivo CSV desde la barra lateral para comenzar.")