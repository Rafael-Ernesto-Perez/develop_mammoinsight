
# Importar las librerías necesarias
import streamlit as st
import pandas as pd
import numpy as np
import calculos_riesgo as cr  # Importa tu módulo con las funciones principales
from calcular_riesgo_ajustado import calcular_riesgo_ajustado
from interpretar_riesgo import interpretar_riesgo

# Función para cargar el contenido de un archivo
def cargar_contenido(archivo):
    with open(archivo, 'r', encoding='utf-8') as file:
        contenido = file.read().strip()  # Usar .strip() para eliminar espacios en blanco o nuevas líneas
    return contenido

# Configuración de Streamlit
st.set_page_config(
    page_title='Calculadora de Riesgo de Cáncer de Mama',
    page_icon=':ribbon:',  # Emoji de lazo rosa
    layout='centered',  # Centra el contenido
    initial_sidebar_state='expanded'
)

# Estilos CSS personalizados
st.markdown(
    '''
    <style>
    .stApp {
        background-color: #ffffff;
        color: #333333;
    }
    h1, h2, h3, h4 {
        color: #FF69B4;
    }
    .stButton button {
        background-color: #f08080;
        color: white;
    }
    .stNumberInput > label, .stSelectbox > label, .stRadio > label {
        font-weight: bold;
        color: #333333 !important;
    }
    /* Ajuste para los textos de los botones de radio */
    .stRadio > label {
        color: #FF69B4 !important;
    }
    .stRadio div {
        color: #333333 !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# Agregar el logo
# Título y logo
# Agregar el logo centrado
logo_path = "logo_iquibanea.png"
#st.image(logo_path, width=300)
# Agregar CSS global para centrar las imágenes
st.markdown(
    '''
    <style>
    .stImage {
        display: flex;
        justify-content: center;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# Mostrar la imagen centrada
st.image(logo_path, width=300)

st.markdown("<h1 style='text-align: center; color: #FF69B4;'>IQUIBA-NEA Modelo de Riesgo de Cáncer de Mama - Gail</h1>", unsafe_allow_html=True)

# Ruta de archivos CSV (actualiza las rutas según la ubicación en tu sistema)
file_path = 'export/BrCa_lambda1.csv'
file_path2 = 'export/BrCa_lambda2.csv'
file_path3 = 'export/BrCa_1_AR.csv'
file_path4 = 'export/BrCa_beta.csv'

# Sección de datos del paciente
st.header('Datos del Paciente')

age_current = st.number_input('Edad actual del paciente', min_value=20, max_value=89, value=50)
num_biopsies = st.number_input('Número de biopsias mamarias', min_value=0, max_value=99, value=0)
hyperplasia = st.selectbox('Hiperplasia atípica en biopsias', options=[99, 0, 1], format_func=lambda x: 'Desconocido' if x == 99 else 'No' if x == 0 else 'Sí')
age_men = st.number_input('Edad al primer período menstrual', min_value=0, max_value=age_current, value=12)
age_first_child = st.number_input('Edad al primer parto', min_value=0, max_value=age_current, value=19)
num_relatives = st.number_input('Número de parientes de primer grado con cáncer de mama', min_value=0, max_value=99, value=0)
race = st.selectbox('Raza/Etnicidad', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], format_func=lambda x: {
    1: "Blanca", 2: "Afroamericana", 3: "Hispana (Nacida en USA)", 4: "Nativo Americano", 5: "Hispana (Nacida fuera de USA)",
    6: "China", 7: "Japonesa", 8: "Filipina", 9: "Hawaiana", 10: "Islas del Pacífico", 11: "Otra Asiática"
}[x])

# Calcular la edad futura automáticamente sumando 5 años a la edad actual
age_projection = age_current + 5

# Preparar los datos del paciente
data = pd.DataFrame({
    'T1': [age_current],
    'T2': [age_projection],
    'N_Biop': [num_biopsies],
    'HypPlas': [hyperplasia],
    'AgeMen': [age_men],
    'Age1st': [age_first_child],
    'N_Rels': [num_relatives],
    'Race': [race]
})

# Corregir datos si es necesario
data = cr.corregir_datos(data)

# Ajuste basado en historia familiar antes de calcular el riesgo
family_history = st.radio("¿Tiene familiares de primer o segundo grado con cáncer de mama?", ['Ninguno', 'Primer grado', 'Segundo grado'])

if family_history != 'Ninguno':
    age_at_diagnosis = st.number_input('Edad al diagnóstico del familiar más cercano', min_value=0, max_value=age_current, value=45)
    ajustar_riesgo = True
else:
    ajustar_riesgo = False

# Calcular riesgos solo después de recopilar la historia familiar
if st.button('Calcular Riesgo'):
    risk_5_year = cr.absolute_riskreal(file_path, file_path2, file_path3, file_path4, data.assign(T2=age_projection))
    risk_lifetime = cr.absolute_riskreal(file_path, file_path2, file_path3, file_path4, data.assign(T2=90))

    st.subheader('Resultados del Riesgo')
    st.write(f'Riesgo a 5 años: {risk_5_year[0]:.2f}%')
    st.write(f'Riesgo de por vida: {risk_lifetime[0]:.2f}%')

    if ajustar_riesgo:
        adjusted_risk = calcular_riesgo_ajustado(risk_lifetime[0], family_history.lower(), age_at_diagnosis)
        categoria, mensaje = interpretar_riesgo(adjusted_risk)
        st.write(f'Riesgo ajustado: {adjusted_risk:.2f}% - {categoria}')
        st.write(mensaje)
    else:
        st.write('Sin ajuste de riesgo adicional basado en historia familiar.')

    import html
    # Mostrar el contenido del archivo con CSS aplicado para un tamaño de fuente específico
    contenido = cargar_contenido('informacion_gail.txt')

    # Escapar caracteres especiales HTML para evitar interpretación
    #contenido_escapado = html.escape(contenido)

    # Usar st.markdown para mostrar el contenido con estilos CSS
    st.markdown(
        f'''
        <div style="background-color: #ffffff; color: #000000; padding: 10px; border: 1px solid #d3d3d3; border-radius: 4px; font-size: 0.8em; line-height: 1.2;">
            {contenido}
        </div>
        ''',
        unsafe_allow_html=True
    )

