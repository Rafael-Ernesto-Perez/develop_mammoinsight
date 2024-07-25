
import streamlit as st
import numpy as np

# Coeficientes del modelo de Gail (simplificados para este ejemplo)
coef = {
    "edad": 0.1,
    "edad_menarca": 0.05,
    "edad_primer_parto": 0.07,
    "num_familiares_cancer": 0.15,
    "num_biopsias": 0.1,
    "hiperplasia": 0.2,
    "raza": {
        "Blanca": 1.0,
        "Afroamericana": 0.9,
        "Hispana/Latina": 0.8,
        "Asiática": 0.7,
        "Nativa Americana": 0.6
    }
}

# Mapeo de rangos de edad al primer parto a valores numéricos
edad_primer_parto_map = {
    "Nunca": 0,
    "<20": 18,
    "20-24": 22,
    "25-29": 27,
    "30 o más": 32
}

# Función para calcular el riesgo
def modelo_gail(edad, edad_menarca, edad_primer_parto, num_familiares_cancer, num_biopsias, hiperplasia, raza):
    edad_primer_parto_valor = edad_primer_parto_map[edad_primer_parto]
    riesgo = (coef["edad"] * edad +
              coef["edad_menarca"] * edad_menarca +
              coef["edad_primer_parto"] * edad_primer_parto_valor +
              coef["num_familiares_cancer"] * num_familiares_cancer +
              coef["num_biopsias"] * num_biopsias +
              coef["hiperplasia"] * hiperplasia +
              coef["raza"][raza])
    return riesgo

# Definir la función del modelo de Gail en Streamlit
def modelo_gail_streamlit():
    #st.title(" IQUIBA-NEA Modelo de Riesgo de Cáncer de Mama - Gail")
    logo_url = "logo_iquibanea.png"
    cols = st.columns([1, 8])
    with cols[0]:
        st.image(logo_url, width=300)
    with cols[1]:
        st.write("<div style='display: flex; align-items: center;'><h1 style='margin: 0; padding-left: 230px;'>IQUIBA-NEA Modelo de Riesgo de Cáncer de Mama - Gail</h1></div>", unsafe_allow_html=True)

    edad = st.slider("Edad", 35, 85, 50)
    raza = st.selectbox("Raza/Etnia", ["Blanca", "Afroamericana", "Hispana/Latina", "Asiática", "Nativa Americana"])
    edad_menarca = st.selectbox("Edad de la primera menstruación", [str(i) for i in range(7, 17)])
    edad_primer_parto = st.selectbox("Edad al primer parto a término", ["Nunca", "<20", "20-24", "25-29", "30 o más"])
    num_familiares_cancer = st.selectbox("Número de familiares de primer grado con cáncer de mama", [str(i) for i in range(0, 11)])
    num_biopsias = st.selectbox("Número de biopsias de mama previas", [str(i) for i in range(0, 11)])
    hiperplasia = st.radio("Historia de hiperplasia atípica en biopsias previas", ["No", "Sí"])
    hiperplasia_val = 1 if hiperplasia == "Sí" else 0

    if st.button("Calcular Riesgo"):
        riesgo = modelo_gail(int(edad), int(edad_menarca), edad_primer_parto, int(num_familiares_cancer), int(num_biopsias), hiperplasia_val, raza)
        st.write(f"El riesgo calculado de cáncer de mama es: {riesgo:.2f}")

# Ejecutar la aplicación Streamlit
if __name__ == "__main__":
    modelo_gail_streamlit()
    