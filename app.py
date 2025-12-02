# app.py – Sistema ACRJ – ICI v7
# Evaluación automática de sentencias penales basadas en prueba indiciaria

import streamlit as st
import pandas as pd

from extractores import leer_pdf, leer_word, limpiar_texto
from evaluador import calcular_ici_v7          # <- motor versión 7
from incongruencias import analizar_incongruencias
from informe_word import generar_informe


# ============================
# CONFIGURACIÓN DE LA PÁGINA
# ============================

st.set_page_config(
    page_title="Auditoría indiciaria – ICI v7",
    layout="wide",
)

st.title("Evaluación automática de sentencias penales basadas en prueba indiciaria")
st.caption("Versión 7 – incorpora el nuevo Criterio C13 de Corroboración Independiente")

st.markdown("---")


# ============================
# FUNCIÓN AUXILIAR
# ============================

def obtener_texto_desde_fuente():
    """
    Lee el texto según la fuente seleccionada:
    - PDF
    - Word (.docx)
    - Texto pegado manualmente
    Devuelve (texto, mensaje_error)
    """
    modo = st.radio(
        "Seleccione la forma de cargar la resolución:",
        ["Pegar texto", "Subir PDF", "Subir Word (.docx)"],
        horizontal=True,
    )

    texto = ""
    error = None

    if modo == "Pegar texto":
        texto = st.text_area(
            "Ingrese o pegue el texto completo de la sentencia / disposición / resolución",
            height=400,
        )
        texto = limpiar_texto(texto)

    elif modo == "Subir PDF":
        archivo_pdf = st.file_uploader(
            "Suba el archivo PDF de la sentencia",
            type=["pdf"],
        )
        if archivo_pdf is not None:
            try:
                texto = leer_pdf(archivo_pdf)
                texto = limpiar_texto(texto)
            except Exception as e:
                error = f"Error al leer el PDF: {e}"

    elif modo == "Subir Word (.docx)":
        archivo_docx = st.file_uploader(
            "Suba el archivo Word (.docx) de la sentencia",
            type=["docx"],
        )
        if archivo_docx is not None:
            try:
                texto = leer_word(archivo_docx)
                texto = limpiar_texto(texto)
            except Exception as e:
                error = f"Error al leer el archivo Word: {e}"

    return texto, error


# ============================
# INTERFAZ PRINCIPAL
# ============================

st.subheader("Ingreso del texto de la sentencia")

texto, error_fuente = obtener_texto_desde_fuente()

if error_fuente:
    st.error(error_fuente)

st.markdown("---")

col_boton, _ = st.columns([1, 3])
with col_boton:
    ejecutar = st.button("🔍 Evaluar sentencia", type="primary")

if ejecutar:
    if not texto:
        st.error("Debe cargar o pegar el texto de la sentencia antes de evaluar.")
    else:
        with st.spinner("Analizando coherencia indiciaria (ICI v7)..."):
            # 1) Cálculo del ICI y criterios C1–C13
            resultados = calcular_ici_v7(texto)

            # 2) Detección de incongruencias lógicas/normativas
            lista_incongruencias = analizar_incongruencias(texto, resultados)

        st.success("Análisis completado.")

        # ============================
        # SECCIÓN 1: RESUMEN GLOBAL
        # ============================

        st.markdown("## 1. Resumen global del ICI")

        criterios = resultados.get("criterios", {}) if isinstance(resultados, dict) else {}

        ici_sin = resultados.get("ICI_sin_penalizacion", None)
        ici_aj = resultados.get("ICI_ajustado", None)
        interpretacion = resultados.get("interpretacion", "")
        frenos = resultados.get("frenos", {})

        col1, col2, col3 = st.columns(3)

        with col1:
            if ici_sin is not None:
                st.metric("ICI sin penalización", f"{ici_sin:.2f}")
            else:
                st.metric("ICI sin penalización", "N/D")

        with col2:
            if ici_aj is not None:
                st.metric("ICI ajustado (con frenos)", f"{ici_aj:.2f}")
            else:
                st.metric("ICI ajustado (con frenos)", "N/D")

        with col3:
            if interpretacion:
                st.write("**Interpretación cualitativa:**")
                st.write(interpretacion)
            else:
                st.write("Sin interpretación generada.")

        if frenos:
            st.info("**Frenos de emergencia / alertas especiales:**")
            for k, v in frenos.items():
                st.write(f"- {k}: {v}")

        # ============================
        # SECCIÓN 2: DETALLE CRITERIOS
        # ============================

        st.markdown("---")
        st.markdown("## 2. Detalle de criterios C1–C13")

        if criterios:
            df_crit = pd.DataFrame(
                [{"Criterio": k, "Puntaje": v} for k, v in criterios.items()]
            ).sort_values("Criterio")
            st.dataframe(df_crit, use_container_width=True)

            st.bar_chart(
                df_crit.set_index("Criterio")["Puntaje"],
                use_container_width=True,
            )
        else:
            st.warning("No se encontraron criterios evaluados en el resultado.")

        # ============================
        # SECCIÓN 3: INCONGRUENCIAS
        # ============================

        st.markdown("---")
        st.markdown("## 3. Incongruencias lógicas y normativas detectadas")

        if not lista_incongruencias:
            st.success("No se detectaron incongruencias relevantes según las reglas heurísticas actuales.")
        else:
            for i, inc in enumerate(lista_incongruencias, start=1):
                with st.expander(f"Incongruencia {i}: {inc.get('tipo', 'Sin tipo')}"):
                    st.write(f"**Tipo:** {inc.get('tipo', 'N/D')}")
                    st.write(f"**Detalle:** {inc.get('detalle', 'Sin detalle')}")
                    parrs = inc.get("parrafos", [])
                    if parrs:
                        st.write(f"**Párrafos implicados:** {parrs}")
                    extractos = inc.get("extractos", [])
                    if extractos:
                        st.write("**Extractos:**")
                        for ex in extractos:
                            st.write(f"- {ex}")

        # ============================
        # SECCIÓN 4: INFORME EN WORD
        # ============================

        st.markdown("---")
        st.markdown("## 4. Generar informe pericial en Word")

        try:
            bytes_docx = generar_informe(texto, resultados, lista_incongruencias)
            st.download_button(
                label="📄 Descargar informe ICI v7 (Word)",
                data=bytes_docx,
                file_name="informe_ici_v7.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        except Exception as e:
            st.error(f"Ocurrió un problema al generar el informe en Word: {e}")

else:
    st.info(
        "Cargue la sentencia (PDF, Word o texto pegado), y luego presione **“Evaluar sentencia”** "
        "para que el sistema calcule el ICI v7 y genere el informe."
    )
