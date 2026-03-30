# Taller 02 Pseudoagente de Consola
# César Orlando Ríos Quieroga

# --- 1. CONFIGURACIÓN INICIAL ---

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

# Lista de diccionarios para gestionar la memoria del agente
# Se inicializa con algunos datos "quemados" para pruebas iniciales
historial_chat = [
    {
        "timestamp": "19/03/2026 07:00:00",
        "cmd": "ping",
        "rol": "admin",
        "descripcion": "se envió un ping y se devuelve un pong"
    }
]

# --- 2. VARIABLES DE CONTROL  PARA EL BOT---

sistema_activo = True    # Se usa para controlar la permanencia en el bucle principal 'while'
intentos = 0             # Contador de intentos para el login 
sesion_iniciada = False  # Bandera para controlar si el usuario ha iniciado sesión correctamente
rol_actual = ""          # Variable para almacenar el rol del usuario actual (admin o invitado)        

# --- 3. MÓDULO DE SEGURIDAD / LOGIN ---

# Usaremos el ciclo while que permite un máximo 3 
while intentos < 3 and not sesion_iniciada:
    # F-string: Muestra dinámicamente el número de intento actual al usuario
    print(f"\n--- INICIO DE SESIÓN (Intento {intentos + 1}/3) ---")
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
        print(f"\n[{rol_actual.upper()}] Comandos: ping, contar, fecha_hoy, validar_pass, calculadora, historial, salir")
    else:
        # Para el invitado visualiza una lista restringida sin la opción de fecha.
        print(f"\n[{rol_actual.upper()}] Comandos: ping, contar, validar_pass, calculadora, historial, salir")

    # Captura la entrada del usuario. 
    # Con .strip() eliminamos los  espacios accidentales al inicio o final.
    cmd_original = input("> ").strip()

    # Usamos el comando a minúsculas (.lower()).
    cmd_lower = cmd_original.lower()
    
    # Se genera variable temporal para guardar la descripción de la acción actual en la memoria
    mensaje_log = ""

    # Opción SALIR
    if cmd_lower == "salir":
        # Se Cambia el estado a False para terminar la ejecución
        sistema_activo = False
        mensaje_log = "Cerrando sesión del agente. ¡Hasta luego!"
        print(mensaje_log)

    # Respuesta al PING con PONG
    elif cmd_lower == "ping":
        # Acción básica de verificación de respuesta del sistema de ping a pong.
        mensaje_log = "se envió un ping y se devuelve un pong"
        print("pong")

    # CONTAR Caracteres
    elif cmd_lower == "contar":
        palabra = input("Ingrese palabra: ").strip()
        vocales = "aeiou"
        c_vocales = 0
        c_consonantes = 0
        
        # Ahora recorre cada elemento de la cadena de texto de forma secuencial. 
        for letra in palabra.lower():
            # Validación: Verifica si el carácter actual pertenece al alfabeto.
            if letra.isalpha():
                # Comprueba si la letra está en el grupo de vocales.
                if letra in vocales:
                    c_vocales += 1 # Incrementa el conteo de vocales halladas.
                else:
                    c_consonantes += 1 # Incrementa el conteo de consonantes halladas.
        
        mensaje_log = f"conteo de palabra '{palabra}': {len(palabra)} letras, {c_vocales} vocales"
        print(f"Total caracteres: {len(palabra)} | Vocales: {c_vocales} | Consonantes: {c_consonantes}")

    # COMANDO: FECHA_HOY (Solo Admin)
    elif cmd_lower == "fecha_hoy":
        # Verifica que solo el rol de administrador puede consultar este dato.
        if rol_actual == "admin":
            # .now(): Captura la fecha y hora exacta del calendario real.
            fecha_real = datetime.now().strftime("%d/%m/%Y")
            mensaje_log = f"Consulta de fecha exitosa: {fecha_real}"
            print(f"La fecha validada del sistema es: {fecha_real}")
        else:
            # Manejo de restricciones: Mensaje de error para usuarios sin privilegios.
            mensaje_log = "Intento fallido de consulta de fecha (Acceso denegado)"
            print("Error: Acceso Denegado. Solo administradores.")

    # COMANDO: VALIDAR_PASS (Nueva lógica implementada)
    elif cmd_lower == "validar_pass":
        # Se solicita la contraseña que se desea analizar
        pass_test = input("Ingrese contraseña a evaluar: ").strip()
        
        # Criterios de evaluación (Lógica complementaria)
        largo_ok = len(pass_test) >= 8
        tiene_num = any(c.isdigit() for c in pass_test)
        tiene_mayus = any(c.isupper() for c in pass_test)
        
        if largo_ok and tiene_num and tiene_mayus:
            print("Resultado: Contraseña SEGURA")
            mensaje_log = f"Validación exitosa (Segura): {pass_test}"
        else:
            print("Resultado: Contraseña DÉBIL")
            print("Sugerencia: Use 8+ caracteres, números y mayúsculas.")
            mensaje_log = f"Validación fallida (Débil): {pass_test}"

    # NUEVO HISTORIAL (Gestión de Memoria)
    elif cmd_lower.startswith("historial"):
        partes = cmd_lower.split()
        
        # HISTORIAL ALL (Muestra todo)
        if len(partes) > 1 and partes[1] == "all":
            mensaje_log = "Visualización completa del historial"
            print("--- HISTORIAL COMPLETO ---")
            for registro in historial_chat:
                print(registro)
        
        # HISTORIAL CLEAR (Limpia la lista)
        elif len(partes) > 1 and partes[1] == "clear":
            historial_chat.clear()
            mensaje_log = "Memoria del historial vaciada correctamente"
            print("Historial eliminado.")
            
        # Búsqueda por palabra clave
        else:
            busqueda = input("Ingrese la palabra clave a buscar: ").strip().lower()
            coincidencias = 0
            print(f"--- Resultados para: '{busqueda}' ---")
            for registro in historial_chat:
                if busqueda in registro["descripcion"].lower():
                    print(f"[{registro['timestamp']}] ({registro['rol']}): {registro['descripcion']}")
                    coincidencias += 1
            
            if coincidencias == 0:
                print("Pseudoagente: No encontré registros que coincidan.")
            mensaje_log = f"Búsqueda realizada con la palabra: {busqueda}"

    # COMANDOS RESTANTES (Calculadora)
    elif cmd_lower == "calculadora":
        # Lógica de calculadora: Manejo de errores con try-except
        try:
            op = input("Operación (+, -, *, /): ").strip()
            n1 = float(input("Número 1: "))
            n2 = float(input("Número 2: "))
         
            
            resultado = 0
            if op == "+": resultado = n1 + n2
            elif op == "-": resultado = n1 - n2
            elif op == "*": resultado = n1 * n2
            elif op == "/": resultado = n1 / n2 if n2 != 0 else "Error: Div por 0"
            else: resultado = "Operación no válida"
            
            print(f"Resultado: {resultado}")
            mensaje_log = f"Uso de calculadora: {n1} {op} {n2} = {resultado}"
        except ValueError:
            print("Error: Ingrese solo números.")
            mensaje_log = "Error de entrada en calculadora"

    else:
        mensaje_log = f"Comando fallido o desconocido: {cmd_lower}"
        print("Comando no reconocido.")

    # --- REGISTRO EN MEMORIA ---
    if mensaje_log != "":
        nuevo_registro = {
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "cmd": cmd_lower,
            "rol": rol_actual,
            "descripcion": mensaje_log
        }
        historial_chat.append(nuevo_registro)

if intentos >= 3:
    print("\nSistema bloqueado. Demasiados intentos fallidos.")