import streamlit as st
import requests
import pandas as pd
from io import BytesIO

#comando: streamlit run mainstreamlit.py
# Configuración de la URL de la API (ajusta el puerto si es necesario)
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Gestión de Taller", layout="wide")

st.title("🚗 Panel de Control - Fachada Taller")

# Sidebar para navegación
st.sidebar.header("Opciones")
menu = st.sidebar.radio("Ir a:", ["Ver Inventario", "Visualizaciones"])

if menu == "Ver Inventario":
    st.subheader("Listado de Vehículos")
    
    if st.button("Cargar/Actualizar Datos"):
        try:
            # Llamada al endpoint de vehículos
            response = requests.get(f"{API_URL}/vehiculos")
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)
                    st.success(f"Se han cargado {len(df)} vehículos.")
                else:
                    st.warning("La base de datos está vacía.")
            else:
                st.error("Error al obtener datos de la API.")
        except Exception as e:
            st.error(f"No se pudo conectar con la API: {e}")

elif menu == "Visualizaciones":
    st.subheader("Análisis Gráfico")
    
    # 1. Selector para el ID del gráfico
    # Puedes usar un selectbox si sabes los nombres, o un number_input
    grafico_id = st.number_input("Seleccione el ID del gráfico", min_value=0, max_value=10, value=0, step=1)
    
    # 2. Botón para realizar la petición
    if st.button("Mostrar Gráfico"):
        try:
            # Llamada al endpoint dinámico usando el ID seleccionado
            with st.spinner(f"Cargando gráfico {grafico_id}..."):
                response = requests.get(f"{API_URL}/grafico/{grafico_id}")
            
            if response.status_code == 200:
                # Convertimos los bytes recibidos en una imagen
                imagen_bytes = BytesIO(response.content)
                st.image(
                    imagen_bytes, 
                    caption=f"Gráfico ID: {grafico_id}", 
                    use_container_width=True
                )
            elif response.status_code == 404:
                st.warning(f"No se encontró ningún gráfico con el ID {grafico_id}.")
            else:
                st.error(f"Error {response.status_code}: No se pudo obtener el gráfico.")
                
        except Exception as e:
            st.error(f"Error de conexión con la API: {e}")

# Pie de página
st.sidebar.info("Conectado a FastAPI Backend")