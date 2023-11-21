from datetime import datetime, timedelta
import sys
import json


class GrafoPonderado:
    def __init__(self):
        self.relaciones = {}
        self.nombres = {}
        self.mensajes_enviados = {}
        self.mensajes_recibidos = {}

    def agregar_persona(self, id_persona, nombre):
        self.nombres[id_persona] = nombre

    def agregar_relacion(self, id_persona_origen, id_persona_destino, peso, fecha):
        if id_persona_origen not in self.relaciones:
            self.relaciones[id_persona_origen] = {}
        if id_persona_destino in self.relaciones[id_persona_origen]:
            self.relaciones[id_persona_origen][id_persona_destino]["peso"] += peso
            self.relaciones[id_persona_origen][id_persona_destino]["fechas"].append(fecha)
        else:
            self.relaciones[id_persona_origen][id_persona_destino] = {"peso": peso, "fechas": [fecha]}
            self.mensajes_enviados[id_persona_origen] = self.mensajes_enviados.get(id_persona_origen, 0) + 1
            self.mensajes_recibidos[id_persona_destino] = self.mensajes_recibidos.get(id_persona_destino, 0) + 1

    def cargar_datos_desde_json(self, datos_mensajes):
        for mensaje in datos_mensajes:
            id_persona_origen = mensaje['id_emisor']
            id_persona_destino = mensaje['id_receptor']
            peso = 1

            # Cambia el formato de fecha aquí
            fecha = datetime.strptime(mensaje['fecha'], '%d/%m/%Y')

            self.agregar_persona(id_persona_origen, mensaje.get('nombre_emisor', ''))
            self.agregar_persona(id_persona_destino, mensaje.get('nombre_receptor', ''))
            self.agregar_relacion(id_persona_origen, id_persona_destino, peso, fecha)
            self.agregar_relacion(id_persona_destino, id_persona_origen, peso, fecha)

    def imprimir_lista_adyacencia(self):
        print("Lista de Adyacencia:")
        for persona, amigos in self.relaciones.items():
            nombre_persona = self.nombres.get(persona, f"Persona-{persona}")
            for amigo, datos in amigos.items():
                nombre_amigo = self.nombres.get(amigo, f"Persona-{amigo}")
                peso = datos["peso"]
                fechas = ', '.join(map(str, datos["fechas"]))
                print(f"{nombre_persona} -> {nombre_amigo}: Peso: {peso}, Fechas: {fechas}")

    def calcular_lapso_tiempo(self):
        # Inicializa las fechas de inicio y fin
        fecha_inicio = None
        fecha_fin = None

        # Inicializa la menor diferencia de tiempo
        menor_diferencia_tiempo = None

        # Inicializa las personas involucradas en la menor diferencia de tiempo
        personas_menor_diferencia = None

        # Itera sobre las relaciones para encontrar las fechas
        for persona1, amigos in self.relaciones.items():
            for persona2, datos in amigos.items():
                fechas = datos["fechas"]

                if fechas:
                    # Obtiene la primera y última fecha en las conversaciones
                    primera_fecha = min(fechas).date()  # Convierte a date
                    ultima_fecha = max(fechas).date()  # Convierte a date

                    # Actualiza las fechas de inicio y fin si es necesario
                    if fecha_inicio is None or primera_fecha < fecha_inicio:
                        fecha_inicio = primera_fecha

                    if fecha_fin is None or ultima_fecha > fecha_fin:
                        fecha_fin = ultima_fecha

                    # Calcula la diferencia de tiempo
                    diferencia_tiempo = ultima_fecha - primera_fecha

                    # Actualiza la menor diferencia de tiempo y las personas involucradas
                    if (
                            menor_diferencia_tiempo is None or diferencia_tiempo < menor_diferencia_tiempo) and diferencia_tiempo.days > 0:
                        menor_diferencia_tiempo = diferencia_tiempo
                        personas_menor_diferencia = (persona1, persona2)

        # Verifica si se encontraron fechas
        if fecha_inicio is not None and fecha_fin is not None and menor_diferencia_tiempo is not None:
            print(
                f"El lapso de tiempo entre la primera y última conversación es de: {menor_diferencia_tiempo.days} días")
            print("")

            if personas_menor_diferencia:
                nombre_persona1 = self.nombres.get(personas_menor_diferencia[0],
                                                   f"Persona-{personas_menor_diferencia[0]}")
                nombre_persona2 = self.nombres.get(personas_menor_diferencia[1],
                                                   f"Persona-{personas_menor_diferencia[1]}")
                print(f"La menor diferencia de tiempo es entre {nombre_persona1} y {nombre_persona2}")
                print("")
        else:
            print("No hay suficientes datos para calcular el lapso de tiempo.")
            print("")

    def personas_con_mas_mensajes(self):
        # Inicializar la pareja con más mensajes
        pareja_con_mas_mensajes = None
        max_mensajes = 0

        # Iterar sobre las relaciones para encontrar la pareja con más mensajes
        for persona1, amigos in self.relaciones.items():
            for persona2, datos in amigos.items():
                mensajes = datos["peso"]

                if mensajes > max_mensajes:
                    max_mensajes = mensajes
                    pareja_con_mas_mensajes = (persona1, persona2)

        # Filtrar las parejas que tienen la misma cantidad de mensajes
        parejas_empatadas = [((self.nombres.get(persona1, f"Persona-{persona1}"),
                               self.nombres.get(persona2, f"Persona-{persona2}")),
                              max_mensajes)
                             for persona1, amigos in self.relaciones.items()
                             for persona2, datos in amigos.items()
                             if datos["peso"] == max_mensajes and persona1 < persona2]

        if pareja_con_mas_mensajes:
            nombre_persona1 = self.nombres.get(pareja_con_mas_mensajes[0], f"Persona-{pareja_con_mas_mensajes[0]}")
            nombre_persona2 = self.nombres.get(pareja_con_mas_mensajes[1], f"Persona-{pareja_con_mas_mensajes[1]}")

            print("Las parejas con mas mensajes son:")
            for (nombre1, nombre2), mensajes in parejas_empatadas:
                print(f"{nombre1} y {nombre2}, con {mensajes} mensajes.")
                print("")
        else:
            print("No hay suficientes datos para determinar la pareja con más mensajes.")
            print("")

        return pareja_con_mas_mensajes, parejas_empatadas

    def cargar_relaciones_desde_json(self, archivo_json):
        with open(archivo_json, 'r') as file:
            datos_relaciones = json.load(file)
        return datos_relaciones

    def elQueTieneMasAmigos(self):
        max_amigos = 0
        max_amigos_persona = None

        for persona, amigos in self.relaciones.items():
            num_amigos = len(amigos)
            if num_amigos > max_amigos:
                max_amigos = num_amigos
                max_amigos_persona = persona

        if max_amigos_persona is not None:
            nombre_max_amigos_persona = self.nombres.get(max_amigos_persona, f"Persona-{max_amigos_persona}")
            print(f"{nombre_max_amigos_persona} tiene la mayor cantidad de amigos con {max_amigos} conexiones.")
            print("")
        else:
            print("No hay información suficiente para determinar quién tiene más amigos.")
            print("")

    def redirigir_salida_a_archivo(self, nombre_archivo):
        salida_original = sys.stdout

        try:
            with open(nombre_archivo, 'w') as archivo_salida:
                sys.stdout = archivo_salida
                # self.calcular_lapso_tiempo()
                # self.personas_con_mas_mensajes()
                # self.elQueTieneMasAmigos()
                self.mensajes_por_mes_por_persona()
                self.mensajes_por_dia_por_pareja()

        finally:
            sys.stdout = salida_original

    def mensajes_por_mes_por_persona(self):
        mensajes_por_mes = {}

        for persona, amigos in self.relaciones.items():
            for amigo, datos in amigos.items():
                for fecha in datos["fechas"]:
                    mes = fecha.strftime('%Y-%m')
                    if mes not in mensajes_por_mes:
                        mensajes_por_mes[mes] = {}
                    if persona not in mensajes_por_mes[mes]:
                        mensajes_por_mes[mes][persona] = 0
                    if amigo not in mensajes_por_mes[mes]:
                        mensajes_por_mes[mes][amigo] = 0

                    mensajes_por_mes[mes][persona] += 1
                    mensajes_por_mes[mes][amigo] += 1

        print("Cantidad de mensajes por mes por persona:")
        for mes, personas in mensajes_por_mes.items():
            print(f"Mes: {mes}")
            for persona, cantidad in personas.items():
                nombre_persona = self.nombres.get(persona, f"Persona-{persona}")
                print(f"{nombre_persona}: {cantidad} mensajes")
            print("")

    def mensajes_por_dia_por_pareja(self):
        mensajes_por_dia_pareja = {}

        for persona, amigos in self.relaciones.items():
            for amigo, datos in amigos.items():
                for fecha in datos["fechas"]:
                    dia = fecha.strftime('%Y-%m-%d')
                    pareja = (persona, amigo)
                    if pareja not in mensajes_por_dia_pareja:
                        mensajes_por_dia_pareja[pareja] = {}
                    if dia not in mensajes_por_dia_pareja[pareja]:
                        mensajes_por_dia_pareja[pareja][dia] = 0

                    mensajes_por_dia_pareja[pareja][dia] += 1

        print("Cantidad de mensajes por día por pareja:")
        for pareja, mensajes_por_dia in mensajes_por_dia_pareja.items():
            nombre_persona1 = self.nombres.get(pareja[0], f"Persona-{pareja[0]}")
            nombre_persona2 = self.nombres.get(pareja[1], f"Persona-{pareja[1]}")
            print(f"Pareja: {nombre_persona1} y {nombre_persona2}")
            for dia, cantidad in mensajes_por_dia.items():
                print(f"Día: {dia}, Mensajes: {cantidad}")
            print("")


if __name__ == "__main__":
    grafo_ponderado = GrafoPonderado()
    datos_mensajes = grafo_ponderado.cargar_relaciones_desde_json('historial_chat.json')
    grafo_ponderado.cargar_datos_desde_json(datos_mensajes)

    # grafo_ponderado.mensajes_por_mes_por_persona()
    # grafo_ponderado.personas_con_mas_mensajes()
    # grafo_ponderado.mensajes_por_dia_por_pareja()
    grafo_ponderado.personas_con_mas_mensajes()
    print("Persona con mas amigos:")
    grafo_ponderado.elQueTieneMasAmigos()
    print("Las personas con una mayor conexion:")
    grafo_ponderado.calcular_lapso_tiempo()
    grafo_ponderado.redirigir_salida_a_archivo('salida_consola.json')

    # Nuevas funcionalidades
