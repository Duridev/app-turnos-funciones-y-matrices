from openpyxl import load_workbook

def leer_parametros(path):
    wb = load_workbook(path, data_only=True)
    ws = wb.active

    full_time = ws["C3"].value
    part_time = ws["C4"].value
    turno = str(ws["C5"].value).strip().upper()

    if full_time is None or part_time is None or turno not in ["A", "B"]:
        raise ValueError("El Excel no contiene valores válidos en C3, C4 o C5.")

    demanda = {}
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    fila_inicio = 8
    for i, dia in enumerate(dias):
        fila = fila_inicio + i
        mañana = ws[f"C{fila}"].value
        inter = ws[f"D{fila}"].value
        tarde = ws[f"E{fila}"].value

        demanda[dia] = {
            "Mañana": mañana if mañana else 0,
            "Intermedio": inter if inter else 0,
            "Tarde": tarde if tarde else 0,
        }

    return full_time, part_time, turno, demanda
