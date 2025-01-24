import streamlit as st
import pandas as pd
import numpy as np

from collections import Counter

from string import ascii_uppercase as mayus
from string import ascii_lowercase as minus

from pages.scripts.funciones_segundo_orden import principal,previaParentesis,previaCompleta,previaContenido


def decimalABinario(n): 
    return "{0:b}".format(int(n))

def letrasSentencia(sentencia):
    diccio = Counter(sentencia)
    letras = []
    for i in diccio:
        if i in mayus or i in minus:
            if i not in letras:
                letras.append(i)

    return letras

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

4. Todas las operaciones se empezarán y terminarán con paréntesis""".format(mayus)

with st.expander("PROGRAMA DE COMPROBACION DE EXPRESIONES LOGICAS"):
    st.markdown(texto)

expresion = st.text_input("Escriba la expresión", value="(A&b)")

comp1 = previaParentesis(expresion)
comp2 = previaCompleta(expresion)
comp3 = previaContenido(expresion)
visible = not (comp1 and comp2 and not comp3)

omega = 1
valor = 0

if st.button("Calcula", disabled = visible):
    letrasS = letrasSentencia(expresion)
    omega,frasefinal,resultado = principal(expresion)
    valor = resultado[frasefinal]

    solu = [resultado[i] for i in letrasS]
    solu.append(resultado[frasefinal])
    Om = decimalABinario(omega)
    soluNp = np.zeros((len(Om),len(letrasS)+1),dtype=bool)
    for j,i in enumerate(solu):
        binarioSol = decimalABinario(i)
        for k in range(len(binarioSol)):
            soluNp[len(Om)-k-1,j] = bool(int(binarioSol[len(binarioSol)-1-k]))
    letrasAux = letrasS.copy()
    letrasAux.append("S")
    df = pd.DataFrame(soluNp,columns=letrasAux)

    st.dataframe(df)