
def interpretar_riesgo(risk):
    # Interpretar el riesgo ajustado en términos de categorías
    if risk < 10:
        return "Bajo riesgo", "Su riesgo es bajo. Se recomienda continuar con las revisiones de rutina."
    elif 10 <= risk <= 20:
        return "Riesgo moderado", "Su riesgo es moderado. Considere discutir con su médico sobre posibles medidas preventivas adicionales."
    else:
        return "Alto riesgo", "Su riesgo es alto. Es importante consultar con un especialista para discutir opciones de seguimiento y prevención."
