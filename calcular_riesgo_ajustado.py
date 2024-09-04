
import pandas as pd
import numpy as np
def calcular_riesgo_ajustado(gail_risk, family_history, age_at_diagnosis):
    # Ajustar el riesgo basado en la historia familiar y la edad de diagnóstico
    if family_history == 'primer grado':
        if age_at_diagnosis >= 50:
            gail_risk *= 1.8
        elif age_at_diagnosis < 50:
            gail_risk *= 2.3
        elif 30 <= age_at_diagnosis < 40:
            gail_risk *= 3.28
        elif 40 <= age_at_diagnosis < 50:
            gail_risk *= 2.56
    elif family_history == 'segundo grado':
        gail_risk *= 1.5
    return gail_risk
