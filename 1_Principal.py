import streamlit as st
from string import ascii_uppercase as mayus
from string import ascii_lowercase as minus

st.title("Resolución de sentencias lógicas")
texto = """PROGRAMA DE COMPROBACION DE EXPRESIONES LOGICAS

- Código escrito y desarrollado por: José Manuel Naveiro Gómez
- Código bajo licencia GPL-V3
------------------------------------------------------------------------
Estructura para las expresiones:
1. Deberán contener las siguientes letras en mayúsculas o minúsculas:
{}
2. Las mayúsculas serán AFIRMACIONES(True) y las minúsculas NEGACIONES(False)
3. Los caracteres especiales para operaciones son:

|Operación|Operador|
|---------|--------|
|AND| & |
|OR| \| |
|NOT| ' |
|implica| > |
|doble implica| : |
|equivalente| = |

4. Todas las operaciones se empezarán y terminarán con paréntesis""".format(mayus)

st.markdown(texto)