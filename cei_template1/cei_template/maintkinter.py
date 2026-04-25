import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from cei_template.Fachadataller import Fachadataller

sys.path.append(os.path.abspath("cei_template"))


class AppTaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión Avanzada de Taller")
        self.root.geometry("900x650")
        
        # 1. Instanciar la Fachada
        try:
            self.fachada = Fachadataller()
        except Exception as e:
            messagebox.showerror("Error", f"Error al inicializar la base de datos: {e}")
            self.root.destroy()
            return
        
        # 2. Configurar Pestañas
        self.tabs = ttk.Notebook(self.root)
        self.tab_tabla = ttk.Frame(self.tabs)
        self.tab_graficos = ttk.Frame(self.tabs)
        
        self.tabs.add(self.tab_tabla, text="Gestión de Flota")
        self.tabs.add(self.tab_graficos, text="Panel de Estadísticas")
        self.tabs.pack(expand=1, fill="both")

        # Variables para almacenar datos y evitar recargar la BD constantemente
        self.lista_figuras = []
        
        # 3. Construir la interfaz
        self.construir_tab_tabla()
        self.construir_tab_graficos()
        
        # 4. Cargar datos iniciales
        self.cargar_tabla()

    # ==========================================
    # PESTAÑA 1: TABLA Y ACCIONES DE VEHÍCULOS
    # ==========================================
    def construir_tab_tabla(self):
        # -- Frame para la tabla --
        frame_arriba = ttk.Frame(self.tab_tabla, padding=10)
        frame_arriba.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(frame_arriba, show='headings')
        scrollbar_y = ttk.Scrollbar(frame_arriba, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar_y.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # -- Frame para acciones inferiores --
        frame_acciones = ttk.LabelFrame(self.tab_tabla, text="Acciones Rápidas", padding=10)
        frame_acciones.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(frame_acciones, text="Matrícula:").pack(side=tk.LEFT, padx=(0, 5))
        self.entry_matricula = ttk.Entry(frame_acciones, width=15)
        self.entry_matricula.pack(side=tk.LEFT, padx=(0, 15))

        btn_reparar = ttk.Button(frame_acciones, text="Reparar Avería", command=self.accion_reparar)
        btn_reparar.pack(side=tk.LEFT, padx=5)

        btn_mantenimiento = ttk.Button(frame_acciones, text="Mantenimiento", command=self.accion_mantenimiento)
        btn_mantenimiento.pack(side=tk.LEFT, padx=5)
        
        btn_actualizar = ttk.Button(frame_acciones, text="Guardar en BD", command=self.accion_actualizar_bd)
        btn_actualizar.pack(side=tk.RIGHT, padx=5)

    def cargar_tabla(self):
        # Limpiar tabla actual
        for item in self.tree.get_children():
            self.tree.delete(item)

        vehiculos = self.fachada.get_vehiculos()
        if not vehiculos:
            return

        # Si flota.data es una lista de objetos, extraemos sus atributos
        if isinstance(vehiculos, list) and hasattr(vehiculos[0], '__dict__'):
            columnas = list(vars(vehiculos[0]).keys())
            filas = [list(vars(v).values()) for v in vehiculos]
        # Si es un DataFrame de Pandas
        elif isinstance(vehiculos, pd.DataFrame):
            columnas = list(vehiculos.columns)
            filas = vehiculos.values.tolist()
        else:
            return # Formato no soportado

        # Configurar columnas
        self.tree["columns"] = columnas
        for col in columnas:
            self.tree.heading(col, text=str(col).upper())
            self.tree.column(col, width=100, anchor=tk.CENTER)

        # Insertar datos
        for fila in filas:
            self.tree.insert("", tk.END, values=fila)

    # -- Métodos de acción --
    def accion_reparar(self):
        matricula = self.entry_matricula.get().strip()
        if not matricula:
            messagebox.showwarning("Atención", "Introduce una matrícula.")
            return
        resultado = self.fachada.reparar_vehiculo(matricula)
        messagebox.showinfo("Resultado", resultado)
        self.cargar_tabla() # Recargar para ver posibles cambios de estado

    def accion_mantenimiento(self):
        matricula = self.entry_matricula.get().strip()
        if not matricula:
            messagebox.showwarning("Atención", "Introduce una matrícula.")
            return
        resultado = self.fachada.realizar_mantenimiento(matricula)
        messagebox.showinfo("Resultado", resultado)
        self.cargar_tabla()

    def accion_actualizar_bd(self):
        try:
            self.fachada.actualizar_base_de_datos()
            messagebox.showinfo("Éxito", "Base de datos actualizada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la BD: {e}")

    # ==========================================
    # PESTAÑA 2: VISUALIZACIÓN DE MÚLTIPLES GRÁFICOS
    # ==========================================
    def construir_tab_graficos(self):
        frame_controles = ttk.Frame(self.tab_graficos, padding=10)
        frame_controles.pack(fill=tk.X)

        ttk.Label(frame_controles, text="Selecciona un gráfico:").pack(side=tk.LEFT, padx=5)
        
        # Nombres de los gráficos basados en tu lista de la Fachada
        opciones_graficos = [
            "1. Cantidad de Vehículos",
            "2. Distribución de Kilometraje",
            "3. Estado de los Vehículos",
            "4. Kilometraje vs Coste",
            "5. Coste por Tipo de Vehículo",
            "6. Averías Más Comunes",
            "7. Nube de Averías"
        ]
        
        self.combo_graficos = ttk.Combobox(frame_controles, values=opciones_graficos, state="readonly", width=35)
        self.combo_graficos.pack(side=tk.LEFT, padx=5)
        self.combo_graficos.bind("<<ComboboxSelected>>", self.cambiar_grafico)
        
        btn_cargar = ttk.Button(frame_controles, text="Generar/Recargar Gráficos", command=self.cargar_graficos)
        btn_cargar.pack(side=tk.LEFT, padx=15)

        # Contenedor donde se pintará la figura de Matplotlib
        self.frame_canvas = ttk.Frame(self.tab_graficos)
        self.frame_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def cargar_graficos(self):
        # Obtenemos la lista de 7 figuras desde la fachada
        try:
            self.lista_figuras = self.fachada.get_lista_graficos()
            self.combo_graficos.current(0) # Seleccionar el primero por defecto
            self.cambiar_grafico(None)
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráficos: {e}")

    def cambiar_grafico(self, event):
        if not self.lista_figuras:
            return       
        indice = self.combo_graficos.current()
        figura = self.lista_figuras[indice]
        for widget in self.frame_canvas.winfo_children():
            widget.destroy()
        if figura:
            canvas = FigureCanvasTkAgg(figura, master=self.frame_canvas)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            ttk.Label(self.frame_canvas, text="No se pudo generar este gráfico.").pack(pady=20)

# ==========================================
# EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AppTaller(root)
    root.mainloop()