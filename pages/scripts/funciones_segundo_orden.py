from collections import Counter
import streamlit as st

from string import hexdigits
from string import ascii_uppercase as mayus
from string import ascii_lowercase as minus

# Comprobacion de misma cantidad de parentesis 
def previaParentesis(sentencia):
    separa = Counter(sentencia)
    pare1 = separa["("]
    pare2 = separa[")"]
    correcto = False
    if pare1 > pare2:
        st.write("faltan ",pare1-pare2," parentesis de cierre")
    elif pare1 < pare2:
        st.write("faltan ",pare2-pare1," parentesis de apertura")
    else:
        correcto = True
        
    return correcto
    
# Comprobacion de misma cantidad de operaciones y parentesis
def previaCompleta(sentencia):
    separa = Counter(sentencia)
    pare1 = separa["("]
    
    operaciones = ["&","|","'",">",":","=","·"]
    opTot = 0
    
    for i in operaciones:
        opTot += separa[i]
    
    correcto = False
    if pare1 > opTot:
        st.write("sobran al menos",pare1-opTot," parentesis para las operaciones")
    elif pare1 < opTot:
        st.write("faltan al menos",opTot-pare1," parentesis para las operaciones")
    else:
        correcto = True
    
    return correcto 
    
# Encontrar letras
def letrasSentencia(sentencia):
    separa = Counter(sentencia)
    letrasf = []
    
    for i in separa:
        if i in mayus:
            ind = mayus.index(i)
            if not ind in letrasf:
                letrasf.append(ind)
        elif i in minus:
            ind = minus.index(i)
            if not ind in letrasf:
                letrasf.append(ind)

    return letrasf                        

# Pasa las letras a numeros para los calculos posteriores
def calcValores(letrasM):
    cant = len(letrasM)
    omega = 2**(2**(cant))-1
    valores = {}

    for i,l in enumerate(letrasM):
        num = 0
        j=2**cant-1
        while j>0:
            for k in range(2**i):
                num += (2**j)
                j -= 1
            for k in range(2**i):
                j -= 1

        valores[l] = num

    return omega, valores

# Preparacion inicial
def preparacionInicial(sentencia):
    todo = Counter(sentencia)
    letrasM = []
    letrasm = []
    for i in todo:
        if i in mayus and i not in letrasM:
            letrasM.append(i)
            letrasm.append(minus[mayus.index(i)])
        elif i in minus and i not in letrasm:
            letrasM.append(mayus[minus.index(i)])
            letrasm.append(i)

    omega, valoresL = calcValores(letrasM)
    for i,j in zip (letrasm, letrasM):
        valoresL[i] = omega - valoresL[j]
    
    return valoresL, omega

# Calcula el nivel maximo de la sentencia
def nivelMax(sentencia):
    nivelM=0
    aux = 0
    for i in sentencia:
         if i == "(":
             aux+=1
         elif i == ")":
             aux-=1
         nivelM=max(nivelM,aux)
             
    return nivelM

# Dice las posiciones de las operaciones en nivel mas profundo
def operacionPosi(sentencia,nivelM):
    operaciones = ["&","|","'",">",":","=","·"]
    nivel=0
    posiOper=[]
    for i,j in enumerate(sentencia):
         if j in operaciones and nivel==nivelM:
             posiOper.append(i)
         elif j=="(":
             nivel+=1
         elif j==")":
             nivel -=1
      
    return posiOper 

# Expresion a calcular
def expresion(sentencia, pos):
    for i,j in enumerate(reversed(sentencia[0:pos])):
        if j == "(":
            posIni = i+1
            break
    for i,j in enumerate(sentencia[pos:]):
        if j == ")":
            posFin = i+1
            break

    return posIni, posFin

# Operacion and
def operAnd(operac,valLetras,nivel):
    letrasInv = operac[1:-1].split("&")

    valor1 = valLetras[letrasInv[0]]
    valor2 = valLetras[letrasInv[1]]
    
    valorS = valor1 & valor2
    nombre = letrasInv[0]+str(0)+letrasInv[1]+str(nivel)
    valLetras[nombre] = valorS

    return valLetras, nombre

# Operacion or
def operOr(operac,valLetras,nivel):
    letrasInv = operac[1:-1].split("|")

    valor1 = valLetras[letrasInv[0]]
    valor2 = valLetras[letrasInv[1]]

    valorS = valor1 | valor2
    nombre = letrasInv[0]+str(1)+letrasInv[1]+str(nivel)
    valLetras[nombre] = valorS

    return valLetras, nombre
    
# Operacion not 
def operNot(operac,valLetras,nivel,omega):
    letrasInv = operac[1:-1].split("'")

    valor1 = valLetras[letrasInv[0]]

    valorS = omega - valor1
    nombre = "-"+letrasInv[0]+str(nivel)
    valLetras[nombre] = valorS

    return valLetras, nombre
    
# Operacion implica (pagina23)
def operImplica(operac,valLetras,nivel,omega):
    letrasInv = operac[1:-1].split(">")

    valor1 = valLetras[letrasInv[0]]
    valor1N = omega - valor1
    valor2 = valLetras[letrasInv[1]]
    valor2N = omega - valor2
    valorS = (valor1N | valor2)
    nombre = letrasInv[0]+str(2)+letrasInv[1]+str(nivel)
    valLetras[nombre] = valorS

    return valLetras, nombre
    
# Operacion dobleImplica (deduccion del implica de la pagina23)
def operDobleImp(operac,valLetras,nivel,omega):
    letrasInv = operac[1:-1].split(":")

    valor1 = valLetras[letrasInv[0]]
    valor1N = omega - valor1
    valor2 = valLetras[letrasInv[1]]
    valor2N = omega - valor2
    valorS = (valor1N | valor2) & (valor2N | valor1)
    nombre = letrasInv[0]+str(3)+letrasInv[1]+str(nivel)
    valLetras[nombre] = valorS

    return valLetras, nombre
    
# Operacion Xor
def operXor(operac,valLetras,nivel,omega):
    letrasInv = operac[1:-1].split("·")
    valor1 = valLetras[letrasInv[0]]
    valor1N = omega - valor1
    valor2 = valLetras[letrasInv[1]]
    valor2N = omega - valor2
    valorS = (valor1 & valor2N) | (valor1N & valor2)
    nombre = letrasInv[0]+str(4)+letrasInv[1]+str(nivel)
    valLetras[nombre] = valorS

    return valLetras, nombre

# Operacion equivalencia 
def operEquivale(operac,valLetras,nivel, omega):
    letrasInv = operac[1:-1].split("=")

    valor1 = valLetras[letrasInv[0]]
    valor2 = valLetras[letrasInv[1]]
    if valor1 == valor2:
        valorS = omega
    else:
        valorS = 0
    nombre = letrasInv[0]+str(5)+letrasInv[1]+str(nivel)
    valLetras[nombre] = valorS

    return valLetras, nombre
    
# Extrae las operaciones de la sentencia en las posiciones indicadas
def extraeOperacion(sentencia,posiOper,valoresL,omega,nivel):
    operaciones = ["&","|","'",">",":","=","·"]
    valores = sentencia
    for i in posiOper:
        oper = operaciones.index(sentencia[i])
        posIni,posFin = expresion(sentencia,i)
        operac = sentencia[i-posIni:i+posFin] 
        if oper == 0:
            valoresL, nombre = operAnd(operac,valoresL,nivel)
            valores = valores.replace(operac,nombre)
            # print(valores)
        elif oper == 1:
            valoresL, nombre = operOr(operac,valoresL,nivel)
            valores = valores.replace(operac,nombre)
            # print(valores)
        elif oper == 2:
            valoresL, nombre = operNot(operac,valoresL,nivel,omega)
            valores = valores.replace(operac,nombre)
            # print(valores)
        elif oper == 3:
            valoresL, nombre = operImplica(operac,valoresL,nivel,omega)
            valores = valores.replace(operac,nombre)
            # print(valores)
        elif oper == 4:
            valoresL, nombre = operDobleImp(operac,valoresL,nivel,omega)
            valores = valores.replace(operac,nombre)
            # print(valores)
        elif oper == 5:
            valoresL, nombre = operEquivale(operac,valoresL,nivel,omega)
            valores = valores.replace(operac,nombre)
            # print(valores)
        elif oper == 6:
            valoresL, nombre = operXor(operac,valoresL,nivel,omega)
            valores = valores.replace(operac,nombre)
        else:
            pass
    return valores, valoresL

def principal(frase =  "((A>B)=(a|B))"):
    valoresLetras, omegaS = preparacionInicial(frase)
    frase2 = frase
    nivel = nivelMax(frase2)
    for i in reversed(range(nivel+1)):
        posis = operacionPosi(frase2,i)
        frase2, valoresLetras= extraeOperacion(frase2,posis,valoresLetras,omegaS,i)
    return omegaS,frase2,valoresLetras

def preparacionInicialCombi(sentencias):
    letrasM = []
    letrasm = []
    for i in sentencias:
        todo = Counter(i)
        for j in todo:
            if j in mayus and j not in letrasM:
                if mayus.index(j)<mayus.index("S"):
                    letrasM.append(j)
                    letrasm.append(minus[mayus.index(j)])
            elif j in minus and j not in letrasm:
                if minus.index(j)<minus.index("s"):
                    letrasM.append(mayus[minus.index(j)])
                    letrasm.append(j)

    omega, valoresL = calcValores(letrasM)
    for i,j in zip (letrasm, letrasM):
        valoresL[i] = omega - valoresL[j]
    
    return valoresL, omega

def combinado(sentencias):
    valoresLetras, omegaS = preparacionInicialCombi(sentencias)
    contador = 0
    for frase in sentencias:
        frase2 = frase
        nivel = nivelMax(frase2)
        for i in reversed(range(nivel+1)):
            posis = operacionPosi(frase2,i)
            frase2, valoresLetras= extraeOperacion(frase2,posis,valoresLetras,omegaS,i)
        valoresLetras[mayus[mayus.index("S")+contador]] = valoresLetras[frase2]
        valoresLetras[minus[minus.index("s")+contador]] = omegaS-valoresLetras[frase2]
        contador += 1

    return omegaS,mayus[mayus.index("S")+contador-1],valoresLetras

def combinadoValores(sentencias,A,B,C):
    omegaS = 15
    valoresLetras, omegaS = preparacionInicialCombi(sentencias)
    valLetrasA = [hexdigits.index(i) for i in A]
    valLetrasB = [hexdigits.index(i) for i in B]
    valLetrasC = [hexdigits.index(i) for i in C]

    solucion = ""

    for j,k,l in zip(valLetrasA,valLetrasB,valLetrasC):
        contador = 0
        for frase in sentencias:
            frase2 = frase
            nivel = nivelMax(frase2)
            for i in reversed(range(nivel+1)):
                posis = operacionPosi(frase2,i)
                frase2, valoresLetras= extraeOperacion(frase2,posis,valoresLetras,omegaS,i)
                valoresLetras["A"] = j
                valoresLetras["a"] = omegaS - j
                valoresLetras["B"] = k
                valoresLetras["b"] = omegaS - k
                valoresLetras["C"] = l
                valoresLetras["c"] = omegaS - l
                
                frase2, valoresLetras= extraeOperacion(frase2,posis,valoresLetras,omegaS,i)

        valoresLetras[mayus[mayus.index("S")+contador]] = valoresLetras[frase2]
        valoresLetras[minus[minus.index("s")+contador]] = omegaS-valoresLetras[frase2]

        solucion += hexdigits[hexdigits.index(valoresLetras[frase2])]

        contador += 1

    return omegaS,mayus[mayus.index("S")+contador-1],solucion
