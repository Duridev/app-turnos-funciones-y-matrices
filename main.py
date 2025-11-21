import numpy as np
from leer_excel import leer_parametros


def generar_horario_por_trabajador(matriz_turnos, total_ft, total_pt, descanso_sab, descanso_dom):
    """
    Genera el horario semanal para cada trabajador.
    
    Args:
        matriz_turnos: Matriz 7x3 con cantidad de trabajadores por turno/día
        total_ft: Total de trabajadores full-time
        total_pt: Total de trabajadores part-time
        descanso_sab: Cantidad de FT que descansan el sábado
        descanso_dom: Cantidad de FT que descansan el domingo
    
    Returns:
        dict: Horario semanal de cada trabajador {nombre: {dia: turno}}
    """
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    horarios = {}
    
    # Inicializar horarios para trabajadores Full-time
    for i in range(1, total_ft + 1):
        nombre = f"Trabajador {i:02d}"
        horarios[nombre] = {dia: "Libre" for dia in dias}
    
    # Inicializar horarios para trabajadores Part-time
    for i in range(1, total_pt + 1):
        nombre = f"Part-Time {i:02d}"
        # Part-time tienen "-" de lunes a viernes (no trabajan) y "Libre" en fin de semana
        horarios[nombre] = {}
        for dia in dias:
            if dia in ["Sábado", "Domingo"]:
                horarios[nombre][dia] = "Libre"
            else:
                horarios[nombre][dia] = "-"
    
    # Determinar qué trabajadores FT descansan en fin de semana
    # Primera mitad descansa sábado, segunda mitad descansa domingo
    trabajadores_descansan_sabado = set(range(1, descanso_sab + 1))
    trabajadores_descansan_domingo = set(range(descanso_sab + 1, total_ft + 1))
    
    # Asignar turnos por día
    for i, dia in enumerate(dias):
        manana_count = int(matriz_turnos[i][0])
        intermedio_count = int(matriz_turnos[i][1])
        tarde_count = int(matriz_turnos[i][2])
        
        trabajador_idx = 1
        
        # Asignar Mañana
        for _ in range(manana_count):
            if trabajador_idx <= total_ft:
                # Verificar si este trabajador descansa este día
                if dia == "Sábado" and trabajador_idx in trabajadores_descansan_sabado:
                    trabajador_idx += 1
                    continue
                if dia == "Domingo" and trabajador_idx in trabajadores_descansan_domingo:
                    trabajador_idx += 1
                    continue
                
                nombre = f"Trabajador {trabajador_idx:02d}"
                horarios[nombre][dia] = "Mañana"
                trabajador_idx += 1
        
        # Asignar Intermedio (incluyendo PT en fin de semana)
        intermedio_asignados = 0
        trabajador_idx = 1
        
        while intermedio_asignados < intermedio_count:
            # Intentar asignar FT primero
            if trabajador_idx <= total_ft:
                if dia == "Sábado" and trabajador_idx in trabajadores_descansan_sabado:
                    trabajador_idx += 1
                    continue
                if dia == "Domingo" and trabajador_idx in trabajadores_descansan_domingo:
                    trabajador_idx += 1
                    continue
                
                nombre = f"Trabajador {trabajador_idx:02d}"
                if horarios[nombre][dia] == "Libre":
                    horarios[nombre][dia] = "Intermedio"
                    intermedio_asignados += 1
                trabajador_idx += 1
            else:
                # Si no hay más FT disponibles y es fin de semana, asignar PT
                if dia in ["Sábado", "Domingo"]:
                    pt_idx = intermedio_asignados - (trabajador_idx - total_ft - 1)
                    if pt_idx < total_pt:
                        nombre = f"Part-Time {pt_idx + 1:02d}"
                        horarios[nombre][dia] = "Part-Time"
                        intermedio_asignados += 1
                    else:
                        break
                else:
                    break
        
        # Asignar Tarde (incluyendo PT en fin de semana)
        tarde_asignados = 0
        trabajador_idx = 1
        
        while tarde_asignados < tarde_count:
            # Intentar asignar FT primero
            if trabajador_idx <= total_ft:
                if dia == "Sábado" and trabajador_idx in trabajadores_descansan_sabado:
                    trabajador_idx += 1
                    continue
                if dia == "Domingo" and trabajador_idx in trabajadores_descansan_domingo:
                    trabajador_idx += 1
                    continue
                
                nombre = f"Trabajador {trabajador_idx:02d}"
                if horarios[nombre][dia] == "Libre":
                    horarios[nombre][dia] = "Tarde"
                    tarde_asignados += 1
                trabajador_idx += 1
            else:
                # Si no hay más FT disponibles y es fin de semana, asignar PT
                if dia in ["Sábado", "Domingo"]:
                    pt_idx = tarde_asignados - (trabajador_idx - total_ft - 1)
                    if pt_idx < total_pt:
                        nombre = f"Part-Time {pt_idx + 1:02d}"
                        if horarios[nombre][dia] == "Libre":
                            horarios[nombre][dia] = "Part-Time"
                        tarde_asignados += 1
                    else:
                        break
                else:
                    break
    
    return horarios


def generar_asignacion(TOTAL_FT, TOTAL_PT, tipo, demanda):
    # Convertimos la demanda del Excel a una matriz igual a tu afluencia base
    afluencias = []
    for valores in demanda.values():
        afluencias.append([
            valores["Mañana"],
            valores["Intermedio"],
            valores["Tarde"]
        ])
    afluencias = np.array(afluencias, dtype=float)

    # --- División FT ---
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

    # --- Disponibilidad FT ---
    ft_por_dia = np.array([
        TOTAL_FT, TOTAL_FT, TOTAL_FT, TOTAL_FT, TOTAL_FT,
        TOTAL_FT - descanso_sabado,
        TOTAL_FT - descanso_domingo,
    ])

    # --- Distribución según afluencia ---
    proporciones = afluencias / afluencias.sum(axis=1, keepdims=True)
    asignacion = np.zeros((7, 3), dtype=int)

    for i in range(7):
        raw = proporciones[i] * ft_por_dia[i]
        base = raw.astype(int)
        diff = ft_por_dia[i] - base.sum()

        decimales = raw - base
        indices = np.argsort(decimales)[::-1]

        for j in range(diff):
            base[indices[j]] += 1

        asignacion[i] = base

    # --- PT en fin de semana ---
    asignacion[5][1] += TOTAL_PT
    asignacion[5][2] += TOTAL_PT
    asignacion[6][1] += TOTAL_PT
    asignacion[6][2] += TOTAL_PT

    # Generar horario por trabajador
    horarios_trabajadores = generar_horario_por_trabajador(
        asignacion, TOTAL_FT, TOTAL_PT, descanso_sabado, descanso_domingo
    )

    return asignacion, descanso_sabado, descanso_domingo, horarios_trabajadores
