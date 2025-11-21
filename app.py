import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from leer_excel import leer_parametros
from main import generar_asignacion
from ui_components import DemandaTreeview, TurnosTreeview
from config import COLORS, FONTS, WINDOW_SIZE


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Turnos - Cafetería ☕")
        
        self._configurar_estilos()
        self.root.configure(bg=COLORS['bg_main'])
        self.root.geometry(WINDOW_SIZE)
        
        # Variables internas
        self.path_excel = None
        self.parametros = None
        self.demanda = None
        
        self._crear_interfaz()
    
    def _configurar_estilos(self):
        """Configura los estilos del tema."""
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview",
            background=COLORS['bg_tree'],
            foreground=COLORS['fg_normal'],
            fieldbackground=COLORS['bg_tree'],
            rowheight=32,
            bordercolor=COLORS['border'],
            borderwidth=1,
            font=FONTS['normal'])
        
        style.configure("Treeview.Heading",
            background=COLORS['bg_frame'],
            foreground=COLORS['fg_heading'],
            font=FONTS['bold'])
        
        style.configure("TButton", font=FONTS['normal'], padding=8)
        style.configure("TLabel", foreground=COLORS['fg_normal'], 
                       background=COLORS['bg_frame'], font=FONTS['normal'])
        style.configure("TFrame", background=COLORS['bg_frame'])
        style.configure("Title.TLabel", foreground=COLORS['fg_heading'],
                       background=COLORS['bg_frame'], font=FONTS['title'])
    
    def _crear_interfaz(self):
        """Crea todos los elementos de la interfaz."""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        self._crear_botones(main_frame)
        self._crear_paneles(main_frame)
    
    def _crear_botones(self, parent):
        """Crea los botones de acción."""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="📂 Cargar Excel", 
                  command=self.cargar_excel).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="⚙️ Generar Turnos", 
                  command=self.generar_turnos).pack(side="left", padx=5)
    
    def _crear_paneles(self, parent):
        """Crea los paneles izquierdo y derecho."""
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True, pady=10)
        
        # Panel izquierdo
        left_frame = ttk.Frame(container)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self._crear_panel_izquierdo(left_frame)
        
        # Panel derecho
        right_frame = ttk.Frame(container)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        self._crear_panel_derecho(right_frame)
    
    def _crear_panel_izquierdo(self, parent):
        """Crea el panel de datos del Excel."""
        ttk.Label(parent, text="📊 Datos del Excel", 
                 style="Title.TLabel").pack(pady=(0, 5))
        
        # Parámetros
        params_frame = ttk.Frame(parent)
        params_frame.pack(fill="x", pady=(0, 10))
        
        self.label_fulltime = ttk.Label(params_frame, text="Full-time: -")
        self.label_fulltime.pack(anchor="w", padx=10, pady=2)
        
        self.label_parttime = ttk.Label(params_frame, text="Part-time: -")
        self.label_parttime.pack(anchor="w", padx=10, pady=2)
        
        self.label_turno = ttk.Label(params_frame, text="Turno: -")
        self.label_turno.pack(anchor="w", padx=10, pady=2)
        
        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=5)
        
        # Demanda
        ttk.Label(parent, text="Demanda por Día:", 
                 style="Title.TLabel").pack(pady=(5, 5))
        
        self.demanda_tree = DemandaTreeview(parent)
        self.demanda_tree.frame.pack(fill="both", expand=True)
    
    def _crear_panel_derecho(self, parent):
        """Crea el panel de turnos generados."""
        ttk.Label(parent, text="⚙️ Turnos Generados", 
                 style="Title.TLabel").pack(pady=(0, 5))
        
        self.turnos_tree = TurnosTreeview(parent)
        self.turnos_tree.frame.pack(fill="both", expand=True)
        
        # Info adicional
        info_frame = ttk.Frame(parent)
        info_frame.pack(fill="x", pady=(10, 0))
        
        self.label_descanso_sab = ttk.Label(info_frame, text="Descansan Sábado: -")
        self.label_descanso_sab.pack(anchor="w", padx=10, pady=2)
        
        self.label_descanso_dom = ttk.Label(info_frame, text="Descansan Domingo: -")
        self.label_descanso_dom.pack(anchor="w", padx=10, pady=2)

    def cargar_excel(self):
        """Carga y procesa el archivo Excel."""
        ruta = filedialog.askopenfilename(
            title="Selecciona tu archivo Excel",
            filetypes=[("Excel files", "*.xlsx")]
        )
        
        if not ruta:
            return
        
        self.path_excel = ruta
        
        try:
            full, part, turno, demanda = leer_parametros(ruta)
            self.parametros = (full, part, turno)
            self.demanda = demanda
            self._mostrar_preview(full, part, turno, demanda)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")
    
    def _mostrar_preview(self, ft, pt, turno, demanda):
        """Muestra la vista previa de los datos cargados."""
        self.label_fulltime.config(text=f"Full-time: {ft}")
        self.label_parttime.config(text=f"Part-time: {pt}")
        self.label_turno.config(text=f"Turno: {turno}")
        
        self.demanda_tree.actualizar(demanda)
        
        messagebox.showinfo("Éxito", 
            "✔️ Datos cargados correctamente.\nPresiona «Generar Turnos» para continuar.")
    
    def generar_turnos(self):
        """Genera y muestra los turnos."""
        if not self.parametros or not self.demanda:
            messagebox.showwarning("Advertencia", "Primero carga un Excel.")
            return
        
        full, part, turno = self.parametros
        matriz, descanso_sab, descanso_dom = generar_asignacion(
            full, part, turno, self.demanda
        )
        
        self.turnos_tree.actualizar(matriz)
        
        self.label_descanso_sab.config(text=f"✅ Descansan Sábado: {descanso_sab}")
        self.label_descanso_dom.config(text=f"✅ Descansan Domingo: {descanso_dom}")
        
        messagebox.showinfo("Éxito", "✔️ Turnos generados correctamente.")



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
