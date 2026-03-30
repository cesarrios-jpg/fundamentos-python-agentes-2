# Taller 01 Pseudoagente de Consola
# César Orlando Ríos Quieroga


# --- 1. CONFIGURACIÓN INICIAL  ---

# Se requiero importarla para carga del módulo de calendario para poder tener la fecha actualizada.
from datetime import datetime

# Definición de usuarios y roles usando un diccionario
# Las claves son los nombres de usuario y los valores son sus roles

# Usuario Administrador: 
## Usuario "admin" con contraseña "admin_1234"
# Usuario Invitado: 
## Usuario "invitado" con contraseña "pass_1234"

usuarios = {
    "admin": "admin_1234",
    "invitado": "pass_1234"
}

# --- 2. VARIABLES DE CONTROL  ---

sistema_activo = True    # Se usa para controlar la permanencia en el bucle principal 'while'
intentos = 0             # Contador de intentos para el login 
sesion_iniciada = False  # Bandera para controlar si el usuario ha iniciado sesión correctamente
rol_actual = ""          # Variable para almacenar el rol del usuario actual (admin o invitado)

# --- 3. MÓDULO DE SEGURIDAD / LOGIN ---

# Usaremos el ciclo while que permite un máximo 3 
while intentos < 3 and not sesion_iniciada:
    # F-string: Muestra dinámicamente el número de intento actual al usuario
    print(f"\n--- INICIO DE SESIÓN (Intento {[intentos + 1]}/[3]) ---")
    # Se usa los camndos  .strip() elimina espacios y .lower() normaliza a minúsculas
    user_input = input("Usuario: ").strip().lower()
    # Uso de .strip() para eliminar espacios 
    pass_input = input("Contraseña: ").strip()

    # Verifica si la clave existe en el diccionario y coincide con su valor medianta el coamando if
    if user_input in usuarios and usuarios[user_input] == pass_input:
        # Se actualiza las banderas para romper el ciclo y otorgar acceso
        sesion_iniciada = True
        rol_actual = user_input
        print(f"Bienvenido, acceso concedido como: {rol_actual}")
    else:
        # Incrementarmmos el valor en caso de fallos para gestionar el límite de seguridad establecido
        intentos += 1
        print("Credenciales incorrectas.")

# --- 4. BUCLE PRINCIPAL DEL AGENTE ---

# Se usa la estructura while para mentener el programa activo esperando comandos del usuario.
while sesion_iniciada and sistema_activo:
    # LÓGICA DE MENÚ
    # Se valida el rol para mostrar solo los comandos autorizados.
    if rol_actual == "admin":
        # Para el administrador visualiza la lista completa, incluyendo 'fecha_hoy'. 
        print(f"\n[{rol_actual.upper()}] Comandos: ping, contar, fecha_hoy, validar_pass, calculadora, salir")
    else:
        # Para el invitado visualiza una lista restringida sin la opción de fecha.
        print(f"\n[{rol_actual.upper()}] Comandos: ping, contar, validar_pass, calculadora, salir")

    # Limpiaremos los espacios y estandariza a minúsculas para evitar errores de coincidencia.
    cmd = input("> ").strip().lower()

    # Opción SALIR 
    if cmd == "salir":
        # Se Cambia el estado a False para terminar la ejecución.
        sistema_activo = False
        print("Cerrando sesión del agente. ¡Hasta luego!")

    # Respuesta al PING con PONG
    elif cmd == "ping":
        # Acción básica de verificación de respuesta del sistema de ping a pong.
        print("pong")

    # CONTAR Caracteres 
    elif cmd == "contar":
        palabra = input("Ingrese palabra: ").strip().lower()
        vocales = "aeiou"
        c_vocales = 0
        c_consonantes = 0
        
        # Recorre cada elemento de la cadena de texto de forma secuencial.
        # Se usa la función isalpha() para validar que el carácter sea una letra y evitar contar espacios u otros símbolos.
      
        # Ahora recorre cada elemento de la cadena de texto de forma secuencial. 
        for letra in palabra:
            # Validación: Verifica si el carácter actual pertenece al alfabeto.
            if letra.isalpha():
                # Comprueba si la letra está en el grupo de vocales.
                if letra in vocales:
                    c_vocales += 1 # Incrementa el conteo de vocales halladas. 
                else:
                    c_consonantes += 1 # Incrementa el conteo de vocales halladas.
        print(f"Total caracteres: {len(palabra)} | Vocales: {c_vocales} | Consonantes: {c_consonantes}")

    # COMANDO: FECHA_HOY (Solo Admin)
    elif cmd == "fecha_hoy":
        # Verifica que solo el rol de administrador puede consultar este dato.
        if rol_actual == "admin":
            # .now(): Captura la fecha y hora exacta del calendario real.
            # .strftime(): Formatea el objeto de fecha en un string legible (Día/Mes/Año).
            fecha_real = datetime.now().strftime("%d/%m/%Y")
            print(f"La fecha validada del sistema es: {fecha_real}")
        else:
            # Manejo de restricciones: Mensaje de error para usuarios sin privilegios.
            print("Error: Acceso Denegado. Solo administradores.")

    # COMANDO: VALIDAR_PASS 
    elif cmd == "validar_pass":
        nueva_p = input("Nueva contraseña: ").strip()
        # Evalúa longitud mínima de la nueva contraseñay diferencia respecto al nombre de usuario.
        if len(nueva_p) >= 8 and nueva_p != "invitado":
            print("Contraseña válida.")
        else:
            print("Contraseña rechazada (muy corta o igual al usuario).")

    # COMANDO: CALCULADORA (Gestión de división por 0) 
    elif cmd == "calculadora":
        # Transforma el input (texto) a float para cálculos numéricos.
        op = input("Operación (+, -, *, /): ")
        n1 = float(input("Número 1: "))
        n2 = float(input("Número 2: "))
        
        if op == "+": print(f"Resultado: {n1 + n2}")
        elif op == "-": print(f"Resultado: {n1 - n2}")
        elif op == "*": print(f"Resultado: {n1 * n2}")
        elif op == "/":
            if n2 != 0: # Validación manual sin excepciones no se permite dividir por cero (0)
                print(f"Resultado: {n1 / n2}")
            else:
                print("Error: No se puede dividir por cero.")
        else:
            print("Operación no válida.")

    else:
        print("Comando no reconocido.")

if intentos >= 3:
    print("Sistema bloqueado. Demasiados intentos fallidos.")

    # --- RESUMEN TÉCNICO DE FUNCIONES Y MÉTODOS UTILIZADOS ---

# 1. FUNCIONES DE INTERACCIÓN (ENTRADA/SALIDA)

# print(): 
###   Función de salida que proyecta mensajes y resultados en la consola.
# input(): 
###   Función de entrada que captura datos del usuario como tipo String (STR).
# f-strings: 
### Formato (f"") que permite incrustar variables en cadenas de texto de forma dinámica.

# 2. MÉTODOS DE MANIPULACIÓN DE STRINGS (CADENAS)

# .strip(): 
### Elimina espacios en blanco al inicio y final de una cadena de texto.
# .lower(): 
### Normaliza el texto convirtiéndolo totalmente a minúsculas.
# .upper(): 
### Transforma el texto a mayúsculas, usado aquí para resaltar el rol activo.
# .isalpha(): 
### Método booleano que valida si un carácter pertenece estrictamente al alfabeto.

# 3. FUNCIONES DE CONVERSIÓN Y MEDICIÓN

# float(): 
# Realiza 'Casting' para transformar un STR numérico en un número decimal.
# len(): 
### Función que contabiliza la cantidad total de caracteres en una cadena o elementos en una lista.

# 4. HERRAMIENTAS DE LÓGICA Y TIEMPO

# datetime.now(): 
### Consulta el reloj y calendario real del sistema operativo
# .strftime(): 
### Método de formateo para presentar objetos de fecha en texto legible (ej. DD/MM/AAAA)[cite: 40].

# 5. ESTRUCTURAS DE CONTROL

# while: 
### Bucle iterativo basado en una condición; se usa para mantener el agente activo.
# for: 
### Bucle de iteración finita; ideal para recorrer cada letra de una palabra.
# if-elif-else: 
### Estructura condicional que actúa como el selector de comandos del agente