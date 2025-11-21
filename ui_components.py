"""Componentes de UI reutilizables."""
from tkinter import ttk
from config import DIAS_SEMANA, TURNOS


class DemandaTreeview:
    """Treeview para mostrar la demanda por día."""
    
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(
            self.frame,
            columns=("Día", *TURNOS),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=12
        )
        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.heading("Día", text="Día")
        self.tree.column("Día", width=120, anchor="w")
        
        for turno in TURNOS:
            self.tree.heading(turno, text=turno)
            width = 100 if turno == "Intermedio" else 80
            self.tree.column(turno, width=width, anchor="center")
    
    def actualizar(self, demanda):
        """Actualiza el treeview con los datos de demanda."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for dia, valores in demanda.items():
            self.tree.insert(
                "", "end",
                values=(dia, valores['Mañana'], valores['Intermedio'], valores['Tarde'])
            )


class TurnosTreeview:
    """Treeview para mostrar los turnos generados."""
    
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
            height=10
        )
        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.heading("Día", text="Día")
        self.tree.column("Día", width=120, anchor="w")
        
        for turno in TURNOS:
            self.tree.heading(turno, text=turno)
            self.tree.column(turno, width=120, anchor="center")
    
    def actualizar(self, matriz):
        """Actualiza el treeview con la matriz de turnos."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for i, dia in enumerate(DIAS_SEMANA):
            fila = matriz[i].tolist()
            valores = [dia, fila[0] if len(fila) > 0 else 0, 
                      fila[1] if len(fila) > 1 else 0, 
                      fila[2] if len(fila) > 2 else 0]
            self.tree.insert("", "end", values=valores)


class HorarioTrabajadoresTreeview:
    """Treeview para mostrar el horario semanal de cada trabajador."""
    
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
        
        # Configurar columna de trabajador
        self.tree.heading("Trabajador", text="Trabajador")
        self.tree.column("Trabajador", width=150, anchor="w")
        
        # Configurar columnas de días
        for dia in DIAS_SEMANA:
            self.tree.heading(dia, text=dia)
            self.tree.column(dia, width=110, anchor="center")
    
    def actualizar(self, horarios_trabajadores):
        """Actualiza el treeview con los horarios por trabajador."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for trabajador, horario in horarios_trabajadores.items():
            valores = [trabajador] + [horario[dia] for dia in DIAS_SEMANA]
            self.tree.insert("", "end", values=valores)
