# ============================================================
#  Configuración centralizada del sistema ACRJ – ICI v7
# ============================================================

# Pesos relativos de cada criterio en el cálculo del ICI v7.
# Deben coincidir con la fórmula utilizada en evaluador_v7.py.
PESOS_CRITERIOS = {
    "C1": 0.15,  # Pluralidad de indicios
    "C2": 0.15,  # Fiabilidad de las fuentes
    "C3": 0.15,  # Nexo lógico indicio–hecho
    "C4": 0.20,  # Tratamiento de hipótesis alternativas
    "C5": 0.10,  # Coherencia temporal / espacial
    "C6": 0.10,  # Ausencia de circularidad
    "C7": 0.05,  # Motivación global
    "C13": 0.10  # Corroboración independiente (nuevo criterio v7)
}


def interpretar_ici(ici: float, criterios: dict) -> str:
    """
    Devuelve una interpretación textual del valor del ICI v7.
    Se usan umbrales coherentes con la app y se añaden avisos
    específicos cuando ciertos criterios están especialmente bajos.
    """

    # Tramo principal del ICI
    if ici < 50:
        base = (
            "RIESGO MUY ALTO: la coherencia indiciaria es deficiente o casi inexistente. "
            "La sentencia presenta graves problemas metodológicos en la aplicación del método indiciario."
        )
    elif ici < 65:
        base = (
            "RIESGO ALTO: la motivación indiciaria presenta fallas relevantes. "
            "El razonamiento probatorio es vulnerable en sede de apelación o casación."
        )
    elif ici < 80:
        base = (
            "RIESGO MEDIO: la sentencia tiene una estructura razonable, "
            "pero mantiene debilidades importantes que justifican una revisión crítica."
        )
    else:
        base = (
            "RIESGO BAJO: la motivación indiciaria es, en general, sólida y cumple "
            "con estándares razonables de coherencia y justificación."
        )

    avisos = []

    # Pluralidad de indicios muy baja
    if criterios.get("C1", 100) < 30:
        avisos.append(
            "C1 muy bajo: la estructura probatoria es monocéntrica o descansa "
            "en muy pocos indicios relevantes."
        )

    # Hipótesis alternativas mal tratadas
    if criterios.get("C4", 100) < 40:
        avisos.append(
            "C4 bajo: no se desarrollan ni se descartan adecuadamente hipótesis alternativas "
            "exculpatorias, lo que afecta la presunción de inocencia en su dimensión metodológica."
        )

    # Coherencia temporal / espacial muy débil
    if criterios.get("C5", 100) < 40:
        avisos.append(
            "C5 muy bajo: existen imprecisiones o incoherencias temporales/espaciales que "
            "dificultan reconstruir con claridad la secuencia de hechos imputados."
        )

    # Circularidad o motivación global deficiente
    if criterios.get("C6", 100) < 60:
        avisos.append(
            "C6 bajo: se detectan posibles círculos viciosos en el uso de la prueba "
            "(especialmente en pericias psicológicas o valoraciones que asumen como probado "
            "lo que deberían demostrar)."
        )

    if criterios.get("C7", 100) < 50:
        avisos.append(
            "C7 bajo: la motivación global presenta saltos lógicos, omisiones o contradicciones "
            "que afectan la coherencia del razonamiento."
        )

    # Falta de corroboración independiente
    if criterios.get("C13", 100) < 40:
        avisos.append(
            "C13 muy bajo: no se aprecia corroboración independiente relevante; la estructura "
            "probatoria depende casi exclusivamente de una única fuente (por ejemplo, la declaración "
            "de la víctima), lo que incrementa considerablemente el riesgo de error judicial."
        )

    if avisos:
        return base + " " + " ".join(avisos)

    return base
