"""Componentes de UI reutilizables para la aplicación Tkinter.

Cada clase encapsula un `ttk.Treeview` con su scrollbar y la lógica mínima
para actualizar los datos. Esto permite mantener el código de la interfaz
principal (`app.py`) limpio y centrado en la disposición de los componentes.
"""
from tkinter import ttk
from config import DIAS_SEMANA, TURNOS


class DemandaTreeview:
    """Treeview específico para mostrar la demanda por día.

    - Construye el widget con una scrollbar vertical.
    - Define las columnas: 'Día' y los turnos declarados en `TURNOS`.
    - `actualizar(demanda)` recibe un diccionario y lo muestra en la tabla.
    """

    def __init__(self, parent):
        # Contenedor que permite empaquetar la scrollbar junto al Treeview
        self.frame = ttk.Frame(parent)

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Treeview con columnas dinámicas según `TURNOS`
        self.tree = ttk.Treeview(
            self.frame,
            columns=("Día", *TURNOS),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=8  # filas visibles por defecto
        )
        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

        # Configurar columna del día y anchos por turno
        self.tree.heading("Día", text="Día")
        self.tree.column("Día", width=120, anchor="w")

        for turno in TURNOS:
            self.tree.heading(turno, text=turno)
            # Dar más anchura a 'Intermedio' porque suele ser más largo
            width = 120 if turno == "Intermedio" else 90
            self.tree.column(turno, width=width, anchor="center")

    def actualizar(self, demanda):
        """Refresca el contenido del Treeview usando el diccionario `demanda`.

        `demanda` tiene la forma: { 'Lunes': {'Mañana': x, 'Intermedio': y, 'Tarde': z}, ... }
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

        for dia, valores in demanda.items():
            self.tree.insert(
                "", "end",
                values=(dia, valores['Mañana'], valores['Intermedio'], valores['Tarde'])
            )


class TurnosTreeview:
    """Treeview que muestra la matriz de turnos calculada.

    Similar a `DemandaTreeview` pero pensado para mostrar la salida del
    algoritmo de asignación: número de trabajadores por turno/día.
    """

    def __init__(self, parent):
        self.frame = ttk.Frame(parent)

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        cols = ["Día", *TURNOS]
        self.tree = ttk.Treeview(
            self.frame,
            columns=cols,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=8
        )
        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

        # Columnas y anchos por defecto
        self.tree.heading("Día", text="Día")
        self.tree.column("Día", width=120, anchor="w")

        for turno in TURNOS:
            self.tree.heading(turno, text=turno)
            self.tree.column(turno, width=120, anchor="center")

    def actualizar(self, matriz):
        """Actualiza la tabla con los valores de la matriz (7x3).

        Se espera que `matriz` sea un objeto indexable con 7 filas y 3 columnas
        (por ejemplo una matriz numpy o lista de listas).
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, dia in enumerate(DIAS_SEMANA):
            fila = matriz[i].tolist()
            valores = [dia, fila[0] if len(fila) > 0 else 0,
                      fila[1] if len(fila) > 1 else 0,
                      fila[2] if len(fila) > 2 else 0]
            self.tree.insert("", "end", values=valores)


class HorarioTrabajadoresTreeview:
    """Treeview que muestra el horario semanal de cada trabajador.

    Incluye scroll vertical y horizontal para navegar cuando hay muchos
    trabajadores o cuando la ventana es estrecha.
    """

    def __init__(self, parent):
        self.frame = ttk.Frame(parent)

        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(self.frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        # Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(self.frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        cols = ["Trabajador", *DIAS_SEMANA]
        self.tree = ttk.Treeview(
            self.frame,
            columns=cols,
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            height=20
        )
        self.tree.pack(fill="both", expand=True)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        # Columna de nombre y columnas de días con ancho cómodo por defecto
        self.tree.heading("Trabajador", text="Trabajador")
        self.tree.column("Trabajador", width=150, anchor="w")

        for dia in DIAS_SEMANA:
            self.tree.heading(dia, text=dia)
            self.tree.column(dia, width=110, anchor="center")

    def actualizar(self, horarios_trabajadores):
        """Rellena la tabla con el diccionario de horarios por trabajador.

        `horarios_trabajadores` es un dict con claves como 'Trabajador 01'
        cuya estructura interna es { 'Lunes': 'Mañana', ... }.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

        for trabajador, horario in horarios_trabajadores.items():
            valores = [trabajador] + [horario[dia] for dia in DIAS_SEMANA]
            self.tree.insert("", "end", values=valores)
