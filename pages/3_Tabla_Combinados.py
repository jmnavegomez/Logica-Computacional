import streamlit as st
import pandas as pd
import numpy as np

from collections import Counter

from string import ascii_uppercase as mayus
from string import ascii_lowercase as minus

from pages.scripts.funciones_segundo_orden import combinado,previaParentesis,previaCompleta,previaContenido
from pages.scripts.funciones_segundo_orden import letrasSentencia as ls2


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

def solucionCombinados(listaCombinado):
    letrasS = []
    for k in listaCombinado:
        aux = letrasSentencia(k)
        for l in aux:
            letrasS.extend(l)
    omega,frasefinal,resultado = combinado(listaCombinado)
    letrasF = [mayus[j] for j in sorted(ls2(letrasS))]
    letrasF.append(mayus[(mayus.index("S")+st.session_state["contador"]-1)])
    solu = [resultado[i] for i in letrasF]
    Om = decimalABinario(omega)
    soluNp = np.zeros((len(Om),len(letrasF)),dtype=bool)
    for j,i in enumerate(solu):
        binarioSol = decimalABinario(i)
        for k in range(len(binarioSol)):
            soluNp[len(Om)-k-1,j] = bool(int(binarioSol[len(binarioSol)-1-k]))
    letrasAux = letrasF.copy()
    return omega,letrasAux,soluNp

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
5. Para combinar las expresiones, usar las letras hasta la S para la inicial y las letras a partir de la S para hacer de conectores""".format(mayus)

if not "combinado" in st.session_state:
    st.session_state.combinado = []

if not "contador" in st.session_state:
    st.session_state.contador = 0

def borrado(clave,pos):
    st.session_state[clave].pop(pos)
    st.session_state["contador"] -= 1
    st.rerun()

def reset(clave):
    st.session_state[clave] = []
    st.session_state["contador"] = 0
    st.rerun()

with st.expander("PROGRAMA DE COMPROBACION DE EXPRESIONES LOGICAS"):
    st.markdown(texto)

expresion = st.text_input("Escriba la expresión", value="(A&b)")


comp1 = previaParentesis(expresion)
comp2 = previaCompleta(expresion)
comp3 = previaContenido(expresion)
visible = not (comp1 and comp2 and not comp3)

if st.button("Expresión "+str(st.session_state["contador"]+1),disabled=visible):
    st.session_state["combinado"].append([mayus[(mayus.index("S")+st.session_state["contador"])],expresion])
    st.session_state["contador"] += 1

df0 = pd.DataFrame(st.session_state["combinado"],columns=["Letra","Expresion"])
st.dataframe(df0)

col1, col2 = st.columns(2)

with col1:
    if st.button("Borrado") and st.session_state["contador"]>0:
        borrado("combinado",st.session_state["contador"]-1)

with col2:
    if st.button("Reset"):
        reset("combinado")

omega = 1
valor = 0

listaCombinado = [i[1] for i in st.session_state["combinado"]]

if st.button("Calcula", disabled = not (len(st.session_state["combinado"])>0)):
    omega,letrasAux,soluNp = solucionCombinados(listaCombinado)
    df = pd.DataFrame(soluNp,columns=letrasAux)

    st.dataframe(df)