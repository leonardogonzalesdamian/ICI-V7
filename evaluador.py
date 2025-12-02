# evaluador.py
# Adaptador para el motor de ICI v7

from typing import Dict, Any

from evaluador_v7 import calcular_ici_v7 as motor_ici_v7
from config import interpretar_ici


def calcular_ici_v7(texto: str) -> Dict[str, Any]:
    base = motor_ici_v7(texto) or {}

    criterios = {
        k: v for k, v in base.items() if k.upper().startswith("C")
    }

    ici_bruto = float(base.get("ICI_v7", 0.0))

    ici_sin = ici_bruto
    ici_ajustado = ici_bruto

    interpretacion = interpretar_ici(ici_ajustado, criterios)

    frenos = {}

    if criterios.get("C4", 100) < 40:
        frenos["Hipótesis alternativas débiles"] = (
            "C4 muy bajo: no se analizan ni descartan adecuadamente "
            "hipótesis alternativas exculpatorias."
        )

    if criterios.get("C13", 100) < 40:
        frenos["Sin corroboración independiente"] = (
            "C13 muy bajo: casi no hay evidencia independiente que respalde la tesis condenatoria."
        )

    if ici_ajustado < 40:
        frenos["ICI muy bajo"] = (
            "La coherencia indiciaria es deficiente o casi inexistente."
        )

    return {
        "criterios": criterios,
        "ICI_sin_penalizacion": ici_sin,
        "ICI_ajustado": ici_ajustado,
        "interpretacion": interpretacion,
        "frenos": frenos,
    }
