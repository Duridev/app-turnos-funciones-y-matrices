"""Configuración y constantes del proyecto.

Este archivo centraliza valores reutilizados por la aplicación:
- Paleta de colores del tema oscuro
- Definición de fuentes usadas en los widgets
- Dimensiones globales
- Listas con los días de la semana y los nombres de los turnos

La idea es mantener valores de estilo y constantes en un único lugar
para facilitar cambios posteriores (tema, tamaño de ventana, etc.).
"""

# Colores del tema oscuro usados en la UI.
# - `bg_main`: color de fondo principal de la ventana
# - `bg_frame`: color de fondo para frames y encabezados
# - `bg_tree`: fondo de los Treeview
# - `fg_normal`: color de texto normal
# - `fg_heading`: color de los encabezados
# - `border`: color de los bordes y separadores
COLORS = {
    'bg_main': '#2b2b2b',
    'bg_frame': '#2d2d2d',
    'bg_tree': '#1e1e1e',
    'fg_normal': '#e6e6e6',
    'fg_heading': '#ffffff',
    'border': '#444444'
}

# Fuentes centralizadas. Facilita ajustar el tamaño o la familia utilizada
# en toda la aplicación.
FONTS = {
    'normal': ('Segoe UI', 14),
    'bold': ('Segoe UI', 14, 'bold'),
    'title': ('Segoe UI', 16, 'bold')
}

# Dimensiones y configuración de ventana por defecto.
WINDOW_SIZE = '1140x700'  # ancho x alto en píxeles
ROW_HEIGHT = 32  # altura de fila utilizada en estilos Treeview

# Días de la semana: lista ordenada usada en tablas y generación de horarios.
DIAS_SEMANA = [
    "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"
]

# Turnos disponibles. Mantener estos nombres coherentes con el Excel de entrada
# y con las referencias en el resto del código.
TURNOS = ["Mañana", "Intermedio", "Tarde"]

# Horarios de cada turno (formato: "HH - HH hrs")
# Estos se muestran en la UI y en el informe Excel
SHIFT_HORARIOS = {
    "Mañana": "08 - 16 hrs",
    "Intermedio": "12 - 20 hrs",
    "Tarde": "16 - 24 hrs",
    "Part-Time": "13 - 24 hrs"
}
