import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from leer_excel import leer_parametros
from main import generar_asignacion


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Turnos - Cafetería ☕")

        # ============================
        # Modo oscuro suave
        # ============================
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview",
                background="#1e1e1e",
                foreground="#e6e6e6",
                fieldbackground="#1e1e1e",
                rowheight=32,
                bordercolor="#444444",
                borderwidth=1,
                font=("Segoe UI", 14))

        style.configure("Treeview.Heading",
                background="#2d2d2d",
                foreground="#ffffff",
                font=("Segoe UI", 14, "bold"))

        style.configure("TButton", font=("Segoe UI", 14), padding=8)
        style.configure("TLabel", foreground="#e6e6e6", background="#2d2d2d", font=("Segoe UI", 14))
        style.configure("TFrame", background="#2d2d2d")
        style.configure("Title.TLabel", foreground="#ffffff", background="#2d2d2d", font=("Segoe UI", 16, "bold"))

        self.root.configure(bg="#2b2b2b")
        self.root.geometry("950x700")

        # ============================
        # Variables internas
        # ============================
        self.path_excel = None
        self.parametros = None
        self.demanda = None

        # ============================
        # FRAME PRINCIPAL
        # ============================
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill="both", expand=True)

        # ---------------------------
        # Frame para botones (arriba)
        # ---------------------------
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)

        btn_cargar = ttk.Button(buttons_frame, text="📂 Cargar Excel", command=self.cargar_excel)
        btn_cargar.pack(side="left", padx=5)

        btn_generar = ttk.Button(buttons_frame, text="⚙️ Generar Turnos", command=self.generar_turnos)
        btn_generar.pack(side="left", padx=5)

        # ---------------------------
        # Frame contenedor para las dos áreas de texto
        # ---------------------------
        container_frame = ttk.Frame(main_frame)
        container_frame.pack(fill="both", expand=True, pady=10)

        # ---------------------------
        # Frame IZQUIERDO (Datos del Excel)
        # ---------------------------
        left_frame = ttk.Frame(container_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Etiqueta
        label_excel = ttk.Label(left_frame, text="📊 Datos del Excel", style="Title.TLabel")
        label_excel.pack(pady=(0, 5))

        # Frame para parámetros (arriba)
        params_frame = ttk.Frame(left_frame)
        params_frame.pack(fill="x", pady=(0, 10))

        # Labels para mostrar parámetros
        self.label_fulltime = ttk.Label(params_frame, text="Full-time: -", font=("Segoe UI", 14))
        self.label_fulltime.pack(anchor="w", padx=10, pady=2)
        
        self.label_parttime = ttk.Label(params_frame, text="Part-time: -", font=("Segoe UI", 14))
        self.label_parttime.pack(anchor="w", padx=10, pady=2)
        
        self.label_turno = ttk.Label(params_frame, text="Turno: -", font=("Segoe UI", 14))
        self.label_turno.pack(anchor="w", padx=10, pady=2)

        # Separador
        separator = ttk.Separator(left_frame, orient="horizontal")
        separator.pack(fill="x", pady=5)

        # Label para demanda
        label_demanda = ttk.Label(left_frame, text="Demanda por Día:", style="Title.TLabel", font=("Segoe UI", 16, "bold"))
        label_demanda.pack(pady=(5, 5))

        # Treeview para mostrar demanda
        tree_frame_left = ttk.Frame(left_frame)
        tree_frame_left.pack(fill="both", expand=True)

        scrollbar_left = ttk.Scrollbar(tree_frame_left, orient="vertical")
        scrollbar_left.pack(side="right", fill="y")

        self.tree_demanda = ttk.Treeview(
            tree_frame_left,
            columns=("Día", "Mañana", "Intermedio", "Tarde"),
            show="headings",
            yscrollcommand=scrollbar_left.set,
            height=12
        )
        self.tree_demanda.pack(fill="both", expand=True)
        scrollbar_left.config(command=self.tree_demanda.yview)

        # Configurar columnas
        self.tree_demanda.heading("Día", text="Día")
        self.tree_demanda.heading("Mañana", text="Mañana")
        self.tree_demanda.heading("Intermedio", text="Intermedio")
        self.tree_demanda.heading("Tarde", text="Tarde")

        self.tree_demanda.column("Día", width=120, anchor="w")
        self.tree_demanda.column("Mañana", width=80, anchor="center")
        self.tree_demanda.column("Intermedio", width=100, anchor="center")
        self.tree_demanda.column("Tarde", width=80, anchor="center")

        # ---------------------------
        # Frame DERECHO (Turnos Generados)
        # ---------------------------
        right_frame = ttk.Frame(container_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # Etiqueta
        label_turnos = ttk.Label(right_frame, text="⚙️ Turnos Generados", style="Title.TLabel")
        label_turnos.pack(pady=(0, 5))

        # Treeview para mostrar turnos
        tree_frame_right = ttk.Frame(right_frame)
        tree_frame_right.pack(fill="both", expand=True)

        scrollbar_right = ttk.Scrollbar(tree_frame_right, orient="vertical")
        scrollbar_right.pack(side="right", fill="y")

        # Crear columnas para los 3 turnos
        cols = ["Día", "Mañana", "Intermedio", "Tarde"]
        self.tree_turnos = ttk.Treeview(
            tree_frame_right,
            columns=cols,
            show="headings",
            yscrollcommand=scrollbar_right.set,
            height=10
        )
        self.tree_turnos.pack(fill="both", expand=True)
        scrollbar_right.config(command=self.tree_turnos.yview)

        # Configurar columnas
        self.tree_turnos.heading("Día", text="Día")
        self.tree_turnos.column("Día", width=120, anchor="w")
        
        self.tree_turnos.heading("Mañana", text="Mañana")
        self.tree_turnos.column("Mañana", width=120, anchor="center")
        
        self.tree_turnos.heading("Intermedio", text="Intermedio")
        self.tree_turnos.column("Intermedio", width=120, anchor="center")
        
        self.tree_turnos.heading("Tarde", text="Tarde")
        self.tree_turnos.column("Tarde", width=120, anchor="center")

        # Frame para información adicional
        info_frame = ttk.Frame(right_frame)
        info_frame.pack(fill="x", pady=(10, 0))

        self.label_descanso_sab = ttk.Label(info_frame, text="Descansan Sábado: -", font=("Segoe UI", 14))
        self.label_descanso_sab.pack(anchor="w", padx=10, pady=2)
        
        self.label_descanso_dom = ttk.Label(info_frame, text="Descansan Domingo: -", font=("Segoe UI", 14))
        self.label_descanso_dom.pack(anchor="w", padx=10, pady=2)

    # ====================================================
    # 1. Cargar archivo Excel
    # ====================================================
    def cargar_excel(self):
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
            self.mostrar_preview(full, part, turno, demanda)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

    # ====================================================
    # 2. Vista previa
    # ====================================================
    def mostrar_preview(self, ft, pt, turno, demanda):
        # Actualizar labels de parámetros
        self.label_fulltime.config(text=f"Full-time: {ft}")
        self.label_parttime.config(text=f"Part-time: {pt}")
        self.label_turno.config(text=f"Turno: {turno}")

        # Limpiar treeview de demanda
        for item in self.tree_demanda.get_children():
            self.tree_demanda.delete(item)

        # Llenar treeview con demanda
        for dia, valores in demanda.items():
            self.tree_demanda.insert(
                "",
                "end",
                values=(
                    dia,
                    valores['Mañana'],
                    valores['Intermedio'],
                    valores['Tarde']
                )
            )
        
        messagebox.showinfo("Éxito", "✔️ Datos cargados correctamente.\nPresiona «Generar Turnos» para continuar.")

    # ====================================================
    # 3. Ejecutar algoritmo y mostrar resultado
    # ====================================================
    def generar_turnos(self):
        if not self.parametros or not self.demanda:
            messagebox.showwarning("Advertencia", "Primero carga un Excel.")
            return

        full, part, turno = self.parametros
        demanda = self.demanda

        matriz, descanso_sab, descanso_dom = generar_asignacion(full, part, turno, demanda)

        # Limpiar el treeview de turnos
        for item in self.tree_turnos.get_children():
            self.tree_turnos.delete(item)

        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        # Llenar treeview con la matriz de turnos (solo primeras 3 columnas: Mañana, Intermedio, Tarde)
        for i, dia in enumerate(dias):
            fila = matriz[i].tolist()
            # Tomar solo las primeras 3 columnas que corresponden a Mañana, Intermedio y Tarde
            valores = [dia, fila[0] if len(fila) > 0 else 0, fila[1] if len(fila) > 1 else 0, fila[2] if len(fila) > 2 else 0]
            self.tree_turnos.insert("", "end", values=valores)

        # Actualizar labels de descanso
        self.label_descanso_sab.config(text=f"✅ Descansan Sábado: {descanso_sab}")
        self.label_descanso_dom.config(text=f"✅ Descansan Domingo: {descanso_dom}")
        
        messagebox.showinfo("Éxito", "✔️ Turnos generados correctamente.")


# ====================================================
# Lanzar aplicación
# ====================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
