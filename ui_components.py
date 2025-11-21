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
