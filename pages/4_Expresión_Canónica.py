import streamlit as st
import pandas as pd
import numpy as np

from collections import Counter

from string import ascii_uppercase as mayus
from string import ascii_lowercase as minus

from pages.scripts.funciones_segundo_orden import combinado,previaParentesis,previaCompleta,previaContenido
from pages.scripts.funciones_segundo_orden import calcValores

def calculoCano(datos,filas):
    expresiones = []
    for i in filas:
        sol = datos.iloc[i]
        expr = []
        for j,k in enumerate(sol):
            if k == 1:
                expr.append(mayus[j])
            else:
                expr.append(minus[j])
        expresiones.append("("+"&".join(expr)+")")
    st.write("|".join(expresiones))



def decimalABinario(n): 
    return "{0:b}".format(int(n))


if "siguiente" not in st.session_state:
    st.session_state.siguiente = False

st.title("Resolución de sentencias lógicas")
texto = """
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

4. Todas las operaciones se empezarán y terminarán con paréntesis
5. Poner la cantidad de variables y seleccionar los valores que son verdaderos en la tabla.""".format(mayus)

with st.expander("PROGRAMA DE COMPROBACION DE EXPRESIONES LOGICAS"):
    st.markdown(texto)

valor = st.number_input("Cantidad de variables en la expresión canónica.", value = 0, step = 1, format = "%d", min_value=0)

comp3 = valor>0
visible = not comp3

df = None

letrasS = [i for i in range(valor)]
omega, valoresL = calcValores(letrasS)

Om = decimalABinario(omega)
soluNp = np.zeros((len(Om),len(letrasS)),dtype=bool)
for j,i in enumerate(valoresL):
    binarioSol = decimalABinario(valoresL[i])

    for k in range(len(binarioSol)):
        soluNp[len(Om)-k-1,j] = bool(int(binarioSol[len(binarioSol)-1-k]))
df = pd.DataFrame(soluNp,columns=[ mayus[i] for i in letrasS])

evento = st.dataframe(df,
    key="data",
    on_select="rerun",
    selection_mode=["multi-row", "multi-column"],
)

if st.button("Expresión", disabled = visible):
    calculoCano(df,evento.selection.rows)