import numpy as np
from leer_excel import leer_parametros

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

    return asignacion, descanso_sabado, descanso_domingo
