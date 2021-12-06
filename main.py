import pymongo
import time

conn_str = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)

try:
    client.server_info()
    print("\nConectado con exito a MongoDB")
    time.sleep(1)
except Exception:
    print("Unable to connect to the server.")

def definirAtributos(nombredb, nombrecol, col):
    parar = False
    indice = 1
    listaNomAtr = []
    print("\nVa a pasar a definir los atributos de " + nombredb + "." + nombrecol + ". Este programa solo permite insertar datos del tipo String. Cuando haya terminado de definirlos introduzca un atributo dejando el nombre vacio.\n")
    time.sleep(2)
    while not parar:
        nombreAtr = input("Nombre del atributo nº" + str(indice) + ": ")
        if nombreAtr == "":
            parar = True
        else:
            listaNomAtr.append(nombreAtr)
            indice += 1

    print("\nIntroduzca un valor tipo String para cada uno de estos atributos: ")
    json = {}
    for i in range(0, len(listaNomAtr)):
        json[listaNomAtr[i]] = input("Valor de " + listaNomAtr[i] + ": ")
    col.insert_one(json)


op1 = -1
while not op1 == 0:
    try:
        op1 = int(input("\nBienvenido al programa, introduzca numero:\n0: Salir del programa\n1: Elegir base de datos\n2: Crear base de datos\n3: Borrar base de datos\n--> "))

        if op1 == 1:  # Elegir base de datos
            listabbdd = client.list_database_names()
            print("\nElija base de datos:")
            for i in range(0, len(listabbdd)):
                print(str(i + 1) + ": " + listabbdd[i])
            try:
                selecciondb = listabbdd[int(input("Introduzca numero: ")) - 1]
                print("Ha elegido " + selecciondb)
                db = client.get_database(selecciondb)

                op2 = -1
                while not op2 == 0:
                    op2 = int(input("\nBase de datos seleccionada: " + selecciondb + ", introduzca numero:\n0: Volver\n1: Elegir coleccion\n2: Crear coleccion\n3: Borrar coleccion\n--> "))

                    if op2 == 1:  # Elegir coleccion
                        listacolecciones = db.list_collection_names()
                        if len(listacolecciones) == 0:
                            print("\nNo hay colecciones")
                            time.sleep(2)
                        else:
                            print("\nElija coleccion:")
                            for i in range(0, len(listacolecciones)):
                                print(str(i + 1) + ": " + listacolecciones[i])
                            try:
                                seleccioncol = listacolecciones[int(input("Introduzca numero: ")) - 1]
                                print("Ha elegido " + seleccioncol)
                                col = db.get_collection(seleccioncol)

                                op3 = -1
                                while not op3 == 0:
                                    op3 = int(input("\nColeccion seleccionada: " + selecciondb + "." + seleccioncol + ", introduzca numero:\n0: Volver\n1: Consulta\n2: Insertar datos\n--> "))

                                    if op3 == 1:  # Consulta
                                        try:
                                            ejemplo = list(col.find_one())
                                            print("\nAtributos de un elemento de " + seleccioncol + " (posibles Keys para la consulta)")
                                            for i in range(1, len(ejemplo)):
                                                print(ejemplo[i])
                                            try:
                                                key = input("\nKey: ")
                                                value = input("Value: ")
                                                res = list(col.find({key: value}))
                                                if len(res) == 0:
                                                    print("\nNo se han encontrado coincidencias")
                                                else:
                                                    print("\nSe han encontrado coincidencias:\n")
                                                    for i1 in range(0, len(res)):
                                                        for i2 in range(0, len(ejemplo)):
                                                            print(ejemplo[i2] + ": " + str(res[i1][ejemplo[i2]]))
                                                        print("")
                                                time.sleep(2)
                                            except Exception:
                                                print("\nHa habido un problema con la consulta")
                                        except Exception:
                                            print("\nLa coleccion esta vacia y por tanto sera borrada.")
                                            time.sleep(1)
                                            db.drop_collection(seleccioncol)
                                            print("Se ha borrado " + seleccioncol)
                                            time.sleep(2)

                                    if op3 == 2:  # Insertar datos
                                        try:
                                            json = {}
                                            print("\nInserte valores:")
                                            ejemplo = list(col.find_one())
                                            for i in range(1, len(ejemplo)):
                                                json[ejemplo[i]] = input("Valor de " + ejemplo[i] + ": ")
                                            col.insert_one(json)
                                        except Exception:
                                            print("\nLa coleccion esta vacia y por tanto sera borrada.")
                                            time.sleep(1)
                                            db.drop_collection(seleccioncol)
                                            print("Se ha borrado " + seleccioncol)
                                            time.sleep(2)

                            except Exception:
                                print("\nLa seleccion no es valida")
                                time.sleep(2)

                    if op2 == 2:  # Crear coleccion
                        nombre = input("\nNombre de la coleccion a crear: ")
                        col = db.create_collection(nombre)

                        try:
                            definirAtributos(selecciondb, nombre, col)
                            print("\nLa coleccion " + nombre + " se ha creado con exito")
                            time.sleep(2)
                        except Exception:
                            print("\nHa ocurrido un error al crear la coleccion. Tal vez los datos que ha introducido no sean validos, pruebe otra vez.")
                            time.sleep(2)

                    if op2 == 3:  # Borrar coleccion
                        listacolecciones = db.list_collection_names()
                        if len(listacolecciones) == 0:
                            print("\nNo hay colecciones")
                            time.sleep(2)
                        else:
                            print("\nElija coleccion a borrar:")
                            for i in range(0, len(listacolecciones)):
                                print(str(i + 1) + ": " + listacolecciones[i])
                            print("0: Cancelar operacion y volver al menu")
                            seleccioncol = int(input("Introduzca numero: ")) - 1
                            if not seleccioncol == -1:
                                try:
                                    print("\nHa elegido borrar " + listacolecciones[seleccioncol])
                                    db.drop_collection(listacolecciones[seleccioncol])
                                    time.sleep(2)
                                except Exception:
                                    print("\nLa seleccion no es valida.")
                                    time.sleep(2)

            except Exception:
                print("\nLa seleccion no es valida.")
                time.sleep(2)

        if op1 == 2:  # Crear base de datos
            nombredb = input("\nNombre de la base de datos a crear: ")
            db = client.get_database(nombredb)
            nombrecol = input("Nombre de la coleccion a crear en " + nombredb + ": ")
            col = db.create_collection(nombrecol)

            try:
                definirAtributos(nombredb, nombrecol, col)
                print("\nLa base de datos " + nombredb + " se ha creado con exito")
                time.sleep(2)
            except Exception:
                print("\nHa ocurrido un error al crear la base de datos. Tal vez los datos que ha introducido no sean validos, pruebe otra vez.")
                time.sleep(2)

        if op1 == 3:  # Borrar base de datos
            listabbdd = client.list_database_names()
            print("\nElija base de datos a borrar:")
            for i in range(0, len(listabbdd)):
                print(str(i + 1) + ": " + listabbdd[i])
            print("0: Cancelar operacion y volver al menu")
            selecciondb = int(input("Introduzca numero: ")) - 1
            if not selecciondb == -1:
                try:
                    print("\nHa elegido borrar " + listabbdd[selecciondb])
                    db = client.drop_database(listabbdd[selecciondb])
                    time.sleep(2)
                except Exception:
                    print("\nLa seleccion no es valida")
                    time.sleep(2)

    except Exception:
        print("\nLa seleccion no es valida")
        time.sleep(2)
