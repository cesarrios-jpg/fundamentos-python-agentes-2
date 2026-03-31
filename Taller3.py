###TALLER 3
# Taller 03 Pseudoagente de Consola: Forjando las Herramientas
# César Orlando Ríos Quiroga

# --- 1. CONFIGURACIÓN INICIAL ---

# Se requiere importarla para carga del módulo de calendario para poder tener la fecha actualizada.
from datetime import datetime
# Se requiere importamos para compatibilidad de tipos 
from typing import Dict, List 

# 1. Tus Alias de Tipos: Definir un Alias como 'MemoriaAgente' ayuda a los modelos de IA y a los desarrolladores
# a entender la estructura exacta de los datos que fluyen., 
# la IA sabe que debe procesar un historial con claves y valores de texto predecibles.
type Recuerdo = Dict[str, str]
type MemoriaAgente = List[Recuerdo]

# Definición de usuarios y roles usando un diccionario
usuarios = {
    "admin": "admin_1234",
    "invitado": "pass_1234"
}

# Lista de diccionarios para gestionar la memoria del agente usando el alias de tipo
# Se inicializa con algunos datos "quemados" para pruebas iniciales
historial_chat: MemoriaAgente = [
    {
        "timestamp": "19/03/2026 07:00:00",
        "cmd": "ping",
        "rol": "admin",
        "descripcion": "se envió un ping y se devuelve un pong"
    }
]

# --- 2. DEFINICIÓN DE TOOLS (REFACTORIZACIÓN) ---

def gestionar_historial(accion: str, memoria: MemoriaAgente) -> str:

    # Procesa las acciones del historial (all, clear o búsqueda) y devuelve el resultado formateado.
    partes = accion.lower().split()
    
    # Validamos 'len > 1' para evitar un IndexError al intentar acceder a partes[1].
    # Retorna la representación plana de todos los logs para depuración rápida.
    if len(partes) > 1 and partes[1] == "all":
        resultado = "--- HISTORIAL COMPLETO ---\n"
        for registro in memoria:
            resultado += f"{registro}\n"
        return resultado
    
    # El método .clear() modifica la lista 'memoria' in-place (referencia original).
    elif len(partes) > 1 and partes[1] == "clear":
        # Vaciamos la lista por completo (borrón y cuenta nueva)
        memoria.clear()
        return "Historial eliminado."
        
    # Lógica de búsqueda por palabra clave
    else:
        busqueda = input("Ingrese la palabra clave a buscar: ").strip().lower()
        coincidencias = 0
        resultado = f"--- Resultados para: '{busqueda}' ---\n"
        for registro in memoria:
            if busqueda in registro["descripcion"].lower():
                resultado += f"[{registro['timestamp']}] ({registro['rol']}): {registro['descripcion']}\n"
                coincidencias += 1
        
        if coincidencias == 0:
            return "Pseudoagente: No encontré registros que coincidan."
        return resultado

def contar_letras(palabra: str) -> str:
    
    # Cuenta el total de letras, vocales y consonantes de una cadena.
    vocales = "aeiou"
    c_vocales = 0
    c_consonantes = 0
    
    # Ahora recorre cada elemento de la cadena de texto de forma secuencial. 
    for letra in palabra.lower():
        if letra.isalpha():
            if letra in vocales:
                c_vocales += 1
            else:
                c_consonantes += 1
    
    return f"Total caracteres: {len(palabra)} | Vocales: {c_vocales} | Consonantes: {c_consonantes}"

def validar_password(pass_test: str) -> str:
    
    # Evalúa si una contraseña cumple con criterios mínimos de seguridad.
    
    largo_ok = len(pass_test) >= 8
    tiene_num = any(c.isdigit() for c in pass_test)
    tiene_mayus = any(c.isupper() for c in pass_test)
    
    if largo_ok and tiene_num and tiene_mayus:
        return "Resultado: Contraseña SEGURA"
    else:
        return "Resultado: Contraseña DÉBIL\nSugerencia: Use 8+ caracteres, números y mayúsculas."

def calculadora(op: str, n1: float, n2: float) -> str:
    
    # Realiza operaciones aritméticas básicas y maneja el error de división por cero.
    if op == "+": return str(n1 + n2)
    elif op == "-": return str(n1 - n2)
    elif op == "*": return str(n1 * n2)
    elif op == "/": 
        if n2 == 0:
            return "Error: Div por 0"
        return str(n1 / n2)
    return "Operación no válida"

# --- 3. VARIABLES DE CONTROL ---

sistema_activo = True    # Se usa para controlar la permanencia en el bucle principal 'while'
intentos = 0             # Contador de intentos para el login 
sesion_iniciada = False  # Bandera para controlar si el usuario ha iniciado sesión correctamente
rol_actual = ""          # Variable para almacenar el rol del usuario actual (admin o invitado)        

# --- 4. MÓDULO DE SEGURIDAD / LOGIN ---

# Usaremos el ciclo while que permite un máximo 3 
while intentos < 3 and not sesion_iniciada:
    # F-string: Muestra dinámicamente el número de intento actual al usuario
    print(f"\n--- INICIO DE SESIÓN (Intento {intentos + 1}/3) ---")
    user_input = input("Usuario: ").strip().lower()
    pass_input = input("Contraseña: ").strip()

    # Verifica si la clave existe en el diccionario y coincide con su valor medianta el coamando if
    if user_input in usuarios and usuarios[user_input] == pass_input:
        sesion_iniciada = True
        rol_actual = user_input
        print(f"Bienvenido, acceso concedido como: {rol_actual}")
    else:
        intentos += 1
        print("Credenciales incorrectas.")

# --- 5. BUCLE PRINCIPAL DEL AGENTE (CON BLINDAJE) ---

# Se usa la estructura while para mentener el programa activo esperando comandos del usuario.
while sesion_iniciada and sistema_activo:
    # LÓGICA DE MENÚ
    # Se valida el rol para mostrar solo los comandos autorizados.
    if rol_actual == "admin":
        print(f"\n[{rol_actual.upper()}] Comandos: ping, contar, fecha_hoy, validar_pass, calculadora, historial, salir")
    else:
        print(f"\n[{rol_actual.upper()}] Comandos: ping, contar, validar_pass, calculadora, historial, salir")

    cmd_original = input("> ").strip()
    cmd_lower = cmd_original.lower()
    mensaje_log = ""

    # Implementamos try-except para atrapar errores de permisos y entradas inválidas
    try:
        # Opción SALIR
        if cmd_lower == "salir":
            sistema_activo = False
            mensaje_log = "Cerrando sesión del agente. ¡Hasta luego!"
            print(mensaje_log)

        # Respuesta al PING con PONG
        elif cmd_lower == "ping":
            mensaje_log = "se envió un ping y se devuelve un pong"
            print("pong")

        # CONTAR Caracteres (Refactorizado a Función)
        elif cmd_lower == "contar":
            palabra = input("Ingrese palabra: ").strip()
            resultado_contar = contar_letras(palabra)
            print(resultado_contar)
            mensaje_log = f"conteo de palabra '{palabra}': {resultado_contar}"

        # COMANDO: FECHA_HOY (Blindaje con raise)
        elif cmd_lower == "fecha_hoy":
            # 2. Tu bloque raise:
            # Explicación: Cuando lanzamos un error con 'raise', el programa detiene su ejecución normal 
            # en este punto y busca un bloque 'except' que sepa manejar 'PermissionError'. El error "viaja" 
            # saltando las líneas siguientes hasta llegar al manejador externo en el menú principal.
            if rol_actual == "invitado":
                raise PermissionError("Privilegios insuficientes")
            
            fecha_real = datetime.now().strftime("%d/%m/%Y")
            mensaje_log = f"Consulta de fecha exitosa: {fecha_real}"
            print(f"La fecha validada del sistema es: {fecha_real}")

        # COMANDO: VALIDAR_PASS (Refactorizado a Función)
        # Si el usuario escribió exactamente "validar_pass":
        elif cmd_lower == "validar_pass":
            # Se le solicitamos la clave al usuario y limpiamos espacios  al inicio o final
            pass_test = input("Ingrese contraseña a evaluar (mínimo 8 caracteres, incluir mayúscula, minúscula y número): ").strip()
            resultado_pass = validar_password(pass_test)
            print(resultado_pass)
            mensaje_log = f"Validación de pass: {resultado_pass}"

        # GESTIÓN DE HISTORIAL (Refactorizado a Función)
        # Si el comando escrito por el usuario empieza con la palabra "historial":
        # (Usamos 'startswith' para que funcione aunque escriban "historial all" o "historial clear")

        elif cmd_lower.startswith("historial"):
            resultado_h = gestionar_historial(cmd_lower, historial_chat)
            print(resultado_h)
            mensaje_log = f"Acción historial: {cmd_lower}"

        # COMANDOS RESTANTES (Calculadora con manejo de errores específico)
        # Cuando el ususario elige  "calculadora":
        elif cmd_lower == "calculadora":
            op = input("Operación (+, -, *, /): ").strip()
            # Si el usuario ingresa texto en lugar de números, se disparará un ValueError
            n1 = float(input("Número 1: "))
            n2 = float(input("Número 2: "))
            
            res_calc = calculadora(op, n1, n2)
            print(f"Resultado: {res_calc}")
            mensaje_log = f"Uso de calculadora: {n1} {op} {n2} = {res_calc}"

        else:
            mensaje_log = f"Comando fallido o desconocido: {cmd_lower}"
            print("Comando no reconocido.")

    except PermissionError as e:
        # Atrapamos el error de permisos lanzado por raise
        mensaje_log = f"Acceso denegado: {str(e)}"
        print(f"ALERTA: {str(e)}. No tienes permiso para esta acción.")
    
    except ValueError:
        # Atrapamos errores de conversión numérica en la calculadora
        mensaje_log = "Error de tipo de dato en calculadora"
        print("Error: Entrada inválida. Por favor, ingrese solo números.")

    # --- REGISTRO EN MEMORIA ---
    if mensaje_log != "":
        nuevo_registro: Recuerdo = {
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "cmd": cmd_lower,
            "rol": rol_actual,
            "descripcion": mensaje_log
        }
        historial_chat.append(nuevo_registro)

if intentos >= 3:
    print("\nSistema bloqueado. Demasiados intentos fallidos.")