#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Oct 12 2020

Integrantes del equipo:
    José Ángel García Gómez A01745865
    Erika Marlene García Sánchez A01745158

Funcionalidad del programa:
    El programa se encarga de graficar los diferentes archivos de los casos de
    Sospechosos, Confirmados, Negativos y Defunciones.
    El usuario escoge la gráfica que quiere ver, si quiere ver la de algún
    Estado en específico, a nivel Nacional o una fecha específica.
"""


from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
np.random.seed(19680801)
archivo_default = "Confirmados.csv"


def menu_estados(archivo):
    """
    Esta funcion imprime la lista de todos los estados con la informacion de
    su posicion, nombre del estado y la poblacion de cada estado.

    Parameters
    ----------
    archivo : STR
        Archivo que va a leer para obtener los datos de los estados.

    Returns
    -------
    opciones : Lista
        La lista donde se almacena la opcion del estado que se quiere
        visualizar y el nombre del estado.
    """
    menu = []
    with open(archivo) as archivo:
        linea = archivo.readlines()
        for i in range(1, len(linea)-1):
            menu_renglon = []
            lineas = linea[i]
            num_renglon = lineas.split(",")
            for a in range(1, 3):
                num = num_renglon[a]
                menu_renglon.append(num)
            menu.append(menu_renglon)
    tabla = PrettyTable()
    tabla.field_names = ["No.", "Estado", "Poblacion"]
    estados = []
    for i in range(0, len(linea)-2):
        estado = menu[i][1]
        estados.append(estado)
        poblacion = menu[i][0]
        tabla.add_row([i+1, estado, poblacion])
    print(tabla)
    opcion = int(input("Selecciona un estado (por su numero): "+"\n"))
    while opcion < 1 or opcion > 32:
        print("No es valida esta opcion \n")
        opcion = int(input("Selecciona un estado (por su numero): "+"\n"))
    opciones = [opcion, estados[opcion - 1]]
    return opciones


def menu_usuario():
    opcion_fecha = []
    print("\n")
    tabla_opciones = PrettyTable()
    tabla_opciones.field_names = ["No. ", "Opcion de Gráfica"]
    tabla_opciones.add_row([1, "Por Estado"])
    tabla_opciones.add_row([2, "Nacional"])
    tabla_opciones.add_row([3, "Por fecha en específico"])
    print(tabla_opciones)
    opcion = int(input("Inserte el numero de la opcion deseada: "))
    while opcion < 1 or opcion > 3:
        print("\n Esa opcion no es valida \n")
        print(tabla_opciones)
        opcion = int(input("Por favor, inserte una opcion valida: "))
    if opcion == 3:
        fecha = input("Ingresa la fecha con el formato (dd-mm-yyyy): ")
    else:
        fecha = 0
    opcion_fecha.append(opcion)
    opcion_fecha.append(fecha)
    return opcion_fecha 


def datos_fechas(archivo, step):
    """
    Esta funcion regresa la lista con las fechas que tiene el archivo
    ingresado como parámetro

    Parameters
    ----------
    archivo : STR
        El archivo que se vaya a graficar.
    step : Entero
        Es el espacio entre fechas que se van a obtener para que no se junten
        todas las fechas.

    Returns
    -------
    lista_fechas : List
        La lista de las fechas que se obtienen.

    """
    with open(archivo) as archivo:
        linea = archivo.readlines()[0]
        casos = linea.split(",")
        lista_fechas = casos[3::step]
        return (lista_fechas)


def datos_estado(renglon, archivo, step):
    """
    Esta funcion obtiene los datos de cada estado por fechas.

    Parameters
    ----------
    renglon : Entero
        Es la posicion en la lista de estados donde se encuentra el estado.
    archivo : String
        El archivo que se va a leer para obtener los datos.
    step : Entero
        Es el intervalo entre datos que se va a usar para ir sumando los datos
        dependiendo ese intervalo.

    Returns
    -------
    sumas : Lista
        Es la lista de las sumas de los datos de cada intervalo.

    """
    with open(archivo) as archivo:
        linea = archivo.readlines()[renglon]
        fechas = linea.split(",")
        lista_fechas = fechas[3:]
        lista_enteros = []
        suma = 0
        contador = 0
        sumas = []
        sec_step = step
        for i in lista_fechas:
            i = int(i)
            lista_enteros.append(i)
        for i in range(len(lista_enteros)):
            suma += lista_enteros[i]
            contador += 1
            if contador == sec_step:
                sumas.append(suma)
                suma = 0
                contador = 0
                datos_restantes = (len(lista_enteros)) - (i)
                if (sec_step == step) and datos_restantes < sec_step+1:
                    sec_step = datos_restantes - 1
        return sumas


def menu_archivos():
    """
    Esta funcion despliega el menu de los archivos que se pueden graficar y
    obtiene la opcion que el usuario ingresa.

    Returns
    -------
    indice : Entero
        Es la opcion del archivo que se quiere graficar.

    """
    print("\n"+"Selecciona la opcion que quiere visualizar escribiendo el \
          numero "+"\n")
    tabla_opciones = PrettyTable()
    tabla_opciones.field_names = ["Opcion", "Archivo a leer"]
    tabla_opciones.add_row([1, "Confirmados"])
    tabla_opciones.add_row([2, "Sospehosos"])
    tabla_opciones.add_row([3, "Negativos"])
    tabla_opciones.add_row([4, "Defunciones"])
    tabla_opciones.add_row([5, "Mostrar las 4 graficas"])
    print(tabla_opciones)
    indice = int(input("Inserte la opcion deseada: \n"))
    while indice < 1 or indice > 5:
        print("No es valida esta opcion \n")
        indice = int(input("Vuelva a ingresar una opcion: \n"))
    return indice


def grafica(archivo, estado, frecuencia, datos):
    """
    Esta funcion grafica los datos obtenidos de los archivos.

    Parameters
    ----------
    archivo : string
        Es el archivo que se va a graficar, se usa para ponerle titulo en la
        parte inferior de la gráfica.
    estado : string
        El estado que se va a graficar o si es la fecha, es el título de la
        grafica en la parte superior.
    frecuencia : List
        La lista de datos que se usa para graficar.
    datos : Lista
        Son los datos que aparecen en el eje y.

    Returns
    -------
    None.

    """
    plt.rcdefaults()
    fig, ax = plt.subplots()
    casos = frecuencia
    people = datos
    y_pos = np.arange(len(people))
    error = []
    for i in range(len(people)):
        a = 0
        error.append(a)
    ax.barh(y_pos, casos, xerr=error, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.set_xlabel(archivo)
    ax.set_title(estado)
    plt.show()


def menu_continuar():
    """
    Esta funcion despliega el menu que te pregunta si quieres volver a
    deplegar una grafica o terminar el programa

    Returns
    -------
    opcion : Entero
        Regresa el numero de opcion que el usuario eligió.

    """
    tabla = PrettyTable()
    tabla.field_names = ["Opcion", "Accion"]
    tabla.add_row([1, "Volver a desplegar el menu"])
    tabla.add_row([2, "Terminar Programa"])
    print(tabla)
    opcion = int(input("Selecciona una opcion: "))
    return opcion


def continuar(opcion):
    """
    Esta funcion ejecuta de nuevo el programa si el usuario eligió la opcion 1
    en el menu de continuar y si eligío la opcion dos despliega un mensaje que
    indica que el programa terminó.

    Parameters
    ----------
    opcion : Entero
        Es la opcion que el usuario eligió en el menú de continuar.

    Returns
    -------
    None.

    """
    if opcion == 1:
        main()
    else:
        print("""
            ::::::::::       :::::::::::       ::::    ::: /
            :+:                  :+:           :+:+:   :+: /
            +:+                  +:+           :+:+:+  +:+ /
            :#::+::#             +#+           +#+ +:+ +#+ /
            +#+                  +#+           +#+  +#+#+# /
            #+#                  #+#           #+#   #+#+# /
            ###              ###########       ###    #### /
            """)


def lista_estados(archivo):
    """
    Esta funcion obtiene la lista entera de todos los estados que se
    encuentran en el archivo.

    Parameters
    ----------
    archivo : String
        En este archivo se encuentran los nombres de todos los estados.

    Returns
    -------
    estados : List
        Es la lista con los nombres de todos los estados.

    """
    with open(archivo) as archivo:
        linea = archivo.readlines()
        estados = []
        for i in range(1, len(linea)):
            lineas = linea[i]
            renglon = lineas.split(",")
            estado = renglon[2]
            estados.append(estado)
        return estados


def fechas_completas(archivo):
    """
    Esta funcion obtiene la lista de todas las fechas que se encuentran en el
    archivo que se va a graficar.

    Parameters
    ----------
    archivo : String
        Es el archivo que se va a graficar.

    Returns
    -------
    lista_fechas : Lista
        Es la lista de todas las fechas que hay en el archivo.

    """
    with open(archivo) as archivo:
        linea = archivo.readlines()[0]
        casos = linea.split(",")
        lista_fechas = casos
        return (lista_fechas)


def obtener_columna(fechas, fecha_solicitada):
    """
    Esta funcion obtiene la posicion en el archivo donde se encuentra la fecha
    que ingresó el usuario

    Parameters
    ----------
    fechas : Lista
        La lista de fechas que el archivo que se quiere graficar contiene.
    fecha_solicitada : String
        La fecha del estilo dd-mm-yyyy que ingresó el usuario.

    Returns
    -------
    datos : Lista
            Es la lista que contiene la posicion de la fecha ingresada en el
            archivo y la fecha ingresada.

    """
    datos = []
    for i in range(len(fechas)):
        if fecha_solicitada == fechas[i]:
            datos.append(i)
            datos.append(fecha_solicitada)
            return datos


def obtener_datos_fecha(columna, archivo):
    """
    Esta funcion se encarga de obtener la frecuencia de datos de cada estado
    en la fecha ingresada por el usuario.

    Parameters
    ----------
    columna : Entero
        Es la posición de la fecha que se ingresó en el archivo a graficar.
    archivo : String
        Es el archivo que se va a graficar de donde se va a obtener la
        frecuencia de cada estado.

    Returns
    -------
    casos_int : Lista
        La lista que regresa la frecuencia de casos de cada estado.

    """
    with open(archivo) as archivo:
        linea = archivo.readlines()
        casos = []
        casos_int = []
        for i in range(1, len(linea)):
            lineas = linea[i]
            renglon = lineas.split(",")
            caso = renglon[columna]
            casos.append(caso)
        for a in range(len(casos)):
            enteros = int(casos[a])
            casos_int.append(enteros)
        return casos_int


def accion_graficar(opcion_datos, archivo, fecha_solicitada, indice, nombre):
    """
    Esta funcion obtiene el indice del estado y su nombre, y en caso de que se
    solicite la grafica por fecha en especifico se obtiene la posicion de la
    fecha en el archivo y la fecha que se solicitó

    Parameters
    ----------
    opcion_datos : Entero
        Es la opcion que el usuario eligio de sobre que datos graficar(estado,
        nacional o por fecha).
    archivo : String
        El archivo que se va a graficar.
    fecha_solicitada : String
        La fecha ingresada por el usuario.
    indice : Entero
        El indice del estado que se quiere graficar.
    nombre : String
        El nombre del estado que se quiere graficar.

    Returns
    -------
    datos : Lista
        Contiene la posicion de lo que se quiere graficar y el nombre para
        ponerle titulo a la grafica.

    """
    if opcion_datos == 1:
        datos = [indice, nombre]
    elif opcion_datos == 2:
        datos = [33, "Nacional"]
    elif opcion_datos == 3:
        fechas = fechas_completas(archivo)
        datos = obtener_columna(fechas, fecha_solicitada)
    return datos


def frecuencia_datos(opcion, archivo, opcion_datos, step):
    """
    Esta funcion obtiene la frecuencia de cada estado o fecha segun lo que se
    quiera graficar y tambien obtiene los datos que se van a mostrar y a los
    que se les va a asignar las frecuencias

    Parameters
    ----------
    opcion : Entero
        Es la posicion de lo que se quiere graficar(Ya sea el estado o la
        fecha).
    archivo : String
        El archivo que se va a graficar.
    opcion_datos : Entero
        La opcion que indica que es lo que quiere graficar el usuario(Si por
        estado, nacional o por fecha en específico).
    step : Entero
        El step que se va a utilizar si quiere graficar por estado o nacional.

    Returns
    -------
    regreso : Lista de lista
        La lista que contiene la lista de frecuencia y la lista de los datos
        que se van a mostrar.

    """
    if opcion_datos == 1 or opcion_datos == 2:
        frecuencia = datos_estado(opcion, archivo, step)
        datos = datos_fechas(archivo, step)
    elif opcion_datos == 3:
        frecuencia = obtener_datos_fecha(opcion, archivo)
        datos = lista_estados(archivo)
    regreso = [frecuencia, datos]
    return regreso


def tipo_archivo(opcion):
    """
    Esta función se encarga de asignar el archivo que se quiere graficar

    Parameters
    ----------
    opcion : Entero
        Es la opcion que el usuario ingresó para saber que archivo quiere
        graficar.

    Returns
    -------
    lista : Lista
        Contiene el nombre del archivo a graficar y la opcion que se ingreso
        por el usuario.

    """
    if opcion == 1:
        archivo = "Confirmados.csv"
    elif opcion == 2:
        archivo = "Sospechosos.csv"
    elif opcion == 3:
        archivo = "Negativos.csv"
    elif opcion == 4:
        archivo = "Defunciones.csv"
    elif opcion == 5:
        archivo = ["Confirmados.csv", "Sospechosos.csv", "Negativos.csv",
                   "Defunciones.csv"]
    else:
        print("Opcion no valida")
    lista = [opcion, archivo]
    return lista


def main():
    """
    Esta funcion se encarga de ejecutar todas las funciones para poder correr
    el programa.

    Returns
    -------
    None.

    """
    opcion_tipo_archivo = menu_archivos()
    opcion_datos = menu_usuario()
    opcion_usuario = opcion_datos[0]
    fecha_ingresada = opcion_datos[1]
    lista_archivos = tipo_archivo(opcion_tipo_archivo)
    archivo = lista_archivos[1]
    opcion_archivo = lista_archivos[0]
    estados = si_estados(opcion_usuario)
    indice_estados = estados[0]
    nombre_estado = estados[1]
    step = si_step(opcion_datos[0])
    indice_titulo = datos_ind_tit(opcion_usuario, archivo, fecha_ingresada,
                                  indice_estados, nombre_estado)
    indice_titulo_comprueba = si_lista_lista(indice_titulo)
    indice = indice_titulo_comprueba[0]
    titulo = indice_titulo_comprueba[1]
    graficar(opcion_archivo, archivo, titulo, indice, opcion_datos[0], step)
    continua = menu_continuar()
    continuar(continua)


def si_lista_lista(lista):
    """
    Esta funcion se encarga de saber si la lista ingresada es una lista de
    lista

    Parameters
    ----------
    lista : Lista
        La lista que contiene la posicion y el titulo de lo que se quiere
        graficar.

    Returns
    -------
    lista: Lista
        Es la misma lista que se ingresó, solo se regresa si la lista no es
        lista de lista.
    lista_2: Lista
        Contiene los primeros elementos de cada lista que se encuentra dentro
        de la lista en caso de que la lista ingresada como parámetro sea una
        lista de lista
    """
    lista_funcion = lista[0]
    if not (type(lista_funcion) is list):
        return lista
    else:
        primer_elemento = lista[0][0]
        segundo_elemento = lista[1][1]
        lista_2 = [primer_elemento, segundo_elemento]
        return lista_2


def graficar(opcion, archivo, titulo, indice, segunda_opcion, step):
    """
    Esta funcion se encarga de graficar los archivos.

    Parameters
    ----------
    opcion : Entero
        Es la opcion que el usuario eligió para saber que archivo se quiere
        graficar.
    archivo : String or List
        Si eligio un archivo en especifico se pasa un string, si eligio
        mostrar todas las graficas este va a ser una lista que contiene
        los 4 archivos.
    titulo : String
        Es el titulo que va a tener la grafica(Nombre del estado, nacional o
        la fecha ingresada).
    indice : Entero
        Es la posicion de lo que se quiere graficar en el archivo que se
        eligió.
    segunda_opcion : Entero
        Es la opcion entre (Por estado, nacional o fecha) que el usuario
        ingresó.
    step : Entero
        Si se eligió por estado o nacional este va a ser el intervalo de datos
        que se van a obtener.

    Returns
    -------
    None.

    """
    if opcion >= 1 and opcion < 5:
        x_y = frecuencia_datos(indice, archivo, segunda_opcion, step)
        grafica(archivo, titulo, x_y[0], x_y[1])
    else:
        for i in archivo:
            x_y = frecuencia_datos(indice, i, segunda_opcion, step)
            grafica(i, titulo, x_y[0], x_y[1])


def si_estados(opcion):
    """
    Esta funcion se encarga de evaluar si se eligio que se grafique por estado
    entonces va a mostrar el menu de estados y guardar en una variable lo que
    se regresa de esta funcion

    Parameters
    ----------
    opcion : Entero
        La opcion que el usuario ingresó para  saber si se va a graficar por
        estado o no.

    Returns
    -------
    estados : List
        Si se va a graficar por estado entonces va a tener la posicion del
        estado y el nombre del estado.

    """
    estados = [0, 0]
    if opcion == 1:
        estados = menu_estados(archivo_default)
    return estados


def si_step(opcion):
    """
    Esta funcion evalua si se eligio que fuera por estado o nacional para
    poder pedir el intervalo de datos que el usuario quiera

    Parameters
    ----------
    opcion : Entero
        La opcion que indica si el usuario quiere graficar por estadod o
        nacional.

    Returns
    -------
    step : Entero
        El intervalo de datos que el usuario ingresó en caaso de haber elegido
        graficar por estado o nacional.

    """
    step = 0
    if opcion == 1 or opcion == 2:
        print("\n¿De cuanto en cuanto quieres que se muestre la informacion?")
        step = int(input("(Ej. de 10 en 10, de 15 en 15,etc.)Inserte valor: "))
    return step


def datos_ind_tit(opcion, archivo, fecha, indice, nombre):
    """
    Esta funcion se encarga  de obtener la posicion y el nombre del dato a
    graficar (Ya sea por los estados, el nacional o la fecha ingresada por
    el usuario)

    Parameters
    ----------
    opcion : Entero
        Es la opcion que el usuario eligió entre (por estado, nacional o
        por fecha).
    archivo : String o Lista
        Es el archivo a graficar, si se eligio graficar los 4 archivos se va a
        obtener una lista.
    fecha : String
        Es la fecha ingresada por el usuario.
    indice : Entero
        La posicion en el archivo de lo que se quiere graficar.
    nombre : String
        Es lo que se va a graficar (El estado, Nacional o la fecha ingresada).

    Returns
    -------
    datos: Lista
        Obtiene el indice y el nombre si el archivo ingresado no es lita.
    lista_datos: Lista de lista
        Obtiene la lista de indice y nombre por cada archivo a graficar
    """
    if not (type(archivo) is list):
        datos = accion_graficar(opcion, archivo, fecha, indice, nombre)
        return datos
    else:
        lista_datos = []
        for i in archivo:
            datos = accion_graficar(opcion, i, fecha, indice, nombre)
            lista_datos.append(datos)
        return lista_datos


if __name__ == "__main__":
    main()
