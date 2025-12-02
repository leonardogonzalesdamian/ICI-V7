# ============================================================
#  ACRJ – ICI v7
#  evaluador_v7.py
#  Sistema de Auditoría de Coherencia Razonativa Judicial
# ============================================================

import re

# ------------------------------------------------------------
# C1 – PLURALIDAD DE INDICIOS
# ------------------------------------------------------------
def evaluar_C1(texto: str) -> float:
    t = texto.lower()

    grupos = {
        "testigos": [r"testigo", r"declaraci[oó]n testimonial"],
        "pericias": [r"pericia", r"peritaje"],
        "documentos": [r"documento", r"oficio", r"contrato"],
        "actas": [r"acta", r"intervenci[oó]n"],
        "videos": [r"video", r"grabaci[oó]n"],
        "registros": [r"registro", r"bit[aá]cora"],
    }

    tipos = 0
    for patrones in grupos.values():
        if any(re.search(p, t) for p in patrones):
            tipos += 1

    if tipos == 0:
        return 10
    elif tipos == 1:
        return 40
    elif tipos == 2:
        return 60
    elif tipos == 3:
        return 75
    else:
        return 90


# ------------------------------------------------------------
# C2 – FIABILIDAD DE LAS FUENTES
# ------------------------------------------------------------
def evaluar_C2(texto: str) -> float:
    t = texto.lower()
    puntaje = 20

    if "persist" in t:
        puntaje += 20
    if "coheren" in t:
        puntaje += 20
    if "veros" in t:
        puntaje += 20
    if "corroborad" in t:
        puntaje += 20
    if "contradicci" in t:
        puntaje += 10  

    return min(puntaje, 100)


# ------------------------------------------------------------
# C3 – NEXO LÓGICO
# ------------------------------------------------------------
def evaluar_C3(texto: str) -> float:
    conectores = [
        "por tanto", "por consiguiente", "en consecuencia",
        "se colige", "se desprende", "de ello se concluye"
    ]

    t = texto.lower()
    coincidencias = sum(1 for c in conectores if c in t)

    if coincidencias == 0:
        return 30
    elif coincidencias == 1:
        return 55
    elif coincidencias == 2:
        return 70
    elif coincidencias == 3:
        return 80
    else:
        return 90


# ------------------------------------------------------------
# C4 – HIPÓTESIS ALTERNATIVAS
# ------------------------------------------------------------
def evaluar_C4(texto: str) -> float:
    t = texto.lower()

    menciona = re.search(
        r"hip[oó]tesis alternativa|versi[oó]n exculpatoria|"
        r"otra explicaci[oó]n|error de identificaci[oó]n|defensa del imputado",
        t
    )

    analiza = re.search(
        r"se analiza la versi[oó]n del imputado|se contrasta con la versi[oó]n de la defensa|"
        r"se descarta la hip[oó]tesis",
        t
    )

    if not menciona:
        return 20  
    elif menciona and not analiza:
        return 40  
    else:
        return 75  


# ------------------------------------------------------------
# C5 – COHERENCIA TEMPORAL / ESPACIAL
# ------------------------------------------------------------
def evaluar_C5(texto: str) -> float:
    t = texto.lower()

    fechas = re.findall(r"(19|20)\d{2}", t)
    secuencia = re.findall(
        r"primera ocasi[oó]n|segunda|tercera|posteriormente|con anterioridad|despu[eé]s",
        t
    )

    if not fechas and not secuencia:
        return 30
    elif len(fechas) <= 2 and len(secuencia) <= 2:
        return 55
    elif len(fechas) >= 3 and len(secuencia) >= 2:
        return 70
    else:
        return 80


# ------------------------------------------------------------
# C6 – AUSENCIA DE CIRCULARIDAD
# ------------------------------------------------------------
def evaluar_C6(texto: str) -> float:
    t = texto.lower()

    circular = re.search(
        r"pericia psicol[oó]gica.*agresi[oó]n sexual vivida|"
        r"impacto emocional.*demuestra la agresi[oó]n",
        t
    )

    if circular:
        return 60
    else:
        return 80


# ------------------------------------------------------------
# C7 – MOTIVACIÓN GLOBAL
# ------------------------------------------------------------
def evaluar_C7(texto: str) -> float:
    t = texto.lower()

    secciones = 0
    patrones = [
        "considerando", "fundamento", "motivaci", "an[aá]lisis de la prueba"
    ]

    for p in patrones:
        if p in t:
            secciones += 1

    if secciones == 0:
        return 30
    elif secciones == 1:
        return 50
    elif secciones == 2:
        return 65
    elif secciones == 3:
        return 75
    else:
        return 85


# ------------------------------------------------------------
# C13 – CORROBORACIÓN INDEPENDIENTE (CRITERIO NUEVO)
# ------------------------------------------------------------
def evaluar_C13(texto: str) -> float:
    t = texto.lower()

    evidencias = [
        "certificado médico", "certificado médico legal", "examen médico",
        "pericia de adn", "huella dactilar", "huellas dactilares",
        "cámara de seguridad", "video", "grabación de audio",
        "registro telefónico", "whatsapp", "mensaje de texto",
        "acta de intervención", "acta de registro",
        "acta de incautación", "documento bancario",
        "estado de cuenta", "movimiento bancario",
        "pericia balística", "reconocimiento fotográfico",
        "reconocimiento en rueda",
    ]

    testigos = [
        "testigo presencial", "presenció directamente", "vio cuando", "observó cuando"
    ]

    total = 0

    for palabra in evidencias:
        if palabra in t:
            total += 1
    for frase in testigos:
        if frase in t:
            total += 1

    if total == 0:
        return 10
    elif total == 1:
        return 40
    elif 2 <= total <= 3:
        return 70
    else:
        return 90


# ------------------------------------------------------------
# CÁLCULO DEL ÍNDICE FINAL – ICI v7
# ------------------------------------------------------------
def calcular_ici_v7(texto: str) -> dict:
    C1 = evaluar_C1(texto)
    C2 = evaluar_C2(texto)
    C3 = evaluar_C3(texto)
    C4 = evaluar_C4(texto)
    C5 = evaluar_C5(texto)
    C6 = evaluar_C6(texto)
    C7 = evaluar_C7(texto)
    C13 = evaluar_C13(texto)

    ICI_v7 = (
        0.15 * C1 +
        0.15 * C2 +
        0.15 * C3 +
        0.20 * C4 +
        0.10 * C5 +
        0.10 * C6 +
        0.05 * C7 +
        0.10 * C13
    )

    return {
        "C1": C1, "C2": C2, "C3": C3, "C4": C4,
        "C5": C5, "C6": C6, "C7": C7, "C13": C13,
        "ICI_v7": ICI_v7
    }
