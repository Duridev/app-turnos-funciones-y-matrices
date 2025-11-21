"""Lógica principal para calcular la asignación de turnos.

Este módulo contiene las funciones que convierten la demanda semanal
en una distribución de trabajadores por turno/día y que luego generan
los horarios individuales por trabajador.

Conceptos clave:
- FT (Full-Time): trabajan de lunes a viernes y parte del fin de semana
- PT (Part-Time): trabajan únicamente fines de semana
- Se calculan cuántos FT descansan el sábado y cuántos el domingo
  según el tipo (A/B) y la división de la plantilla.
"""

import numpy as np
from leer_excel import leer_parametros


def generar_horario_por_trabajador(matriz_turnos, total_ft, total_pt, descanso_sab, descanso_dom):
    """Construye un diccionario con el horario semanal de cada trabajador.

    La función distribuye primero a los trabajadores Full-Time (FT) entre
    los turnos de cada día respetando los descansos asignados en fin de semana.
    Si en fin de semana hay necesidad adicional se asignan Part-Time (PT).

    Args:
        matriz_turnos (array-like): Matriz 7x3 con cantidades por día/turno
        total_ft (int): número total de FT
        total_pt (int): número total de PT
        descanso_sab (int): número de FT que descansan el sábado
        descanso_dom (int): número de FT que descansan el domingo

    Returns:
        dict: { 'Trabajador XX': { 'Lunes': 'Mañana', ... }, 'Part-Time XX': {...} }
    """
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    horarios = {}

    # Inicializar todos los FT como 'Libre' por defecto (se asignarán turnos)
    for i in range(1, total_ft + 1):
        nombre = f"Trabajador {i:02d}"
        horarios[nombre] = {dia: "Libre" for dia in dias}

    # Inicializar PT: '-' entre semana (no trabajan) y 'Libre' en fin de semana
    for i in range(1, total_pt + 1):
        nombre = f"Part-Time {i:02d}"
        horarios[nombre] = {}
        for dia in dias:
            if dia in ["Sábado", "Domingo"]:
                horarios[nombre][dia] = "Libre"
            else:
                horarios[nombre][dia] = "-"

    # Determinar índices de FT que descansan cada día del fin de semana.
    # La lógica actual reparte la plantilla en dos mitades.
    trabajadores_descansan_sabado = set(range(1, descanso_sab + 1))
    trabajadores_descansan_domingo = set(range(descanso_sab + 1, total_ft + 1))

    # Asignar por cada día los turnos de Mañana, Intermedio y Tarde
    for i, dia in enumerate(dias):
        manana_count = int(matriz_turnos[i][0])
        intermedio_count = int(matriz_turnos[i][1])
        tarde_count = int(matriz_turnos[i][2])

        # Crear lista de trabajadores FT disponibles para este día
        ft_disponibles = []
        for idx in range(1, total_ft + 1):
            # Saltar FT que descansan este día del fin de semana
            if dia == "Sábado" and idx in trabajadores_descansan_sabado:
                continue
            if dia == "Domingo" and idx in trabajadores_descansan_domingo:
                continue
            ft_disponibles.append(idx)

        # -----------------
        # Asignar Mañana
        # -----------------
        asignados_manana = 0
        for idx in ft_disponibles:
            if asignados_manana >= manana_count:
                break
            nombre = f"Trabajador {idx:02d}"
            horarios[nombre][dia] = "Mañana"
            asignados_manana += 1

        # -----------------
        # Asignar Intermedio
        # Prioriza FT disponibles que aún están libres; si faltan, usa PT en fin de semana
        # -----------------
        asignados_intermedio = 0
        for idx in ft_disponibles:
            if asignados_intermedio >= intermedio_count:
                break
            nombre = f"Trabajador {idx:02d}"
            if horarios[nombre][dia] == "Libre":
                horarios[nombre][dia] = "Intermedio"
                asignados_intermedio += 1

        # Si faltan asignaciones de intermedio y es fin de semana, usar PT
        if asignados_intermedio < intermedio_count and dia in ["Sábado", "Domingo"]:
            pt_idx = 1
            while asignados_intermedio < intermedio_count and pt_idx <= total_pt:
                nombre = f"Part-Time {pt_idx:02d}"
                if horarios[nombre][dia] == "Libre":
                    horarios[nombre][dia] = "Part-Time"
                    asignados_intermedio += 1
                pt_idx += 1

        # -----------------
        # Asignar Tarde
        # Similar a Intermedio: FT disponibles primero, PT en fin de semana si hace falta
        # -----------------
        asignados_tarde = 0
        for idx in ft_disponibles:
            if asignados_tarde >= tarde_count:
                break
            nombre = f"Trabajador {idx:02d}"
            if horarios[nombre][dia] == "Libre":
                horarios[nombre][dia] = "Tarde"
                asignados_tarde += 1

        # Si faltan asignaciones de tarde y es fin de semana, usar PT
        if asignados_tarde < tarde_count and dia in ["Sábado", "Domingo"]:
            pt_idx = 1
            while asignados_tarde < tarde_count and pt_idx <= total_pt:
                nombre = f"Part-Time {pt_idx:02d}"
                if horarios[nombre][dia] == "Libre":
                    horarios[nombre][dia] = "Part-Time"
                    asignados_tarde += 1
                pt_idx += 1

    return horarios


def generar_asignacion(TOTAL_FT, TOTAL_PT, tipo, demanda):
    """Calcula la matriz de asignación por día/turno y genera horarios individuales.

    Pasos principales:
    1. Convertir la `demanda` (diccionario) a una matriz NumPy de afluencias.
    2. Determinar cuántos FT descansan el sábado y el domingo según `tipo`.
    3. Distribuir los FT por turno cada día proporcionalmente a la afluencia.
    4. Añadir PT a los turnos de fin de semana.
    5. Llamar a `generar_horario_por_trabajador` para obtener los horarios por persona.
    """
    # Convertimos la demanda del Excel a una matriz de afluencias
    afluencias = []
    for valores in demanda.values():
        afluencias.append([
            valores["Mañana"],
            valores["Intermedio"],
            valores["Tarde"]
        ])
    afluencias = np.array(afluencias, dtype=float)

    # --- División de la plantilla FT en dos mitades para descanso fin de semana ---
    if TOTAL_FT % 2 == 0:
        mitad1 = mitad2 = TOTAL_FT // 2
    else:
        mitad1 = TOTAL_FT // 2
        mitad2 = TOTAL_FT - mitad1

    if tipo == "A":
        descanso_sabado = mitad1
        descanso_domingo = mitad2
    else:
        descanso_sabado = mitad2
        descanso_domingo = mitad1

    # --- Disponibilidad FT por día (restan los que descansan en finde) ---
    ft_por_dia = np.array([
        TOTAL_FT, TOTAL_FT, TOTAL_FT, TOTAL_FT, TOTAL_FT,
        TOTAL_FT - descanso_sabado,
        TOTAL_FT - descanso_domingo,
    ])

    # --- Distribución proporcional según afluencia por día ---
    proporciones = afluencias / afluencias.sum(axis=1, keepdims=True)
    asignacion = np.zeros((7, 3), dtype=int)

    for i in range(7):
        raw = proporciones[i] * ft_por_dia[i]
        base = raw.astype(int)
        diff = ft_por_dia[i] - base.sum()

        # Repartir las unidades restantes por mayor parte decimal
        decimales = raw - base
        indices = np.argsort(decimales)[::-1]

        for j in range(diff):
            base[indices[j]] += 1

        asignacion[i] = base

    # --- Agregar PT a intermedio y tarde del fin de semana (lógica de negocio) ---
    asignacion[5][1] += TOTAL_PT
    asignacion[5][2] += TOTAL_PT
    asignacion[6][1] += TOTAL_PT
    asignacion[6][2] += TOTAL_PT

    # Generar horarios por trabajador (FT y PT)
    horarios_trabajadores = generar_horario_por_trabajador(
        asignacion, TOTAL_FT, TOTAL_PT, descanso_sabado, descanso_domingo
    )

    return asignacion, descanso_sabado, descanso_domingo, horarios_trabajadores
