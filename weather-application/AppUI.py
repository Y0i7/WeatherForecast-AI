import threading
import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

from WeatherForecaster import WeatherForecaster, CONTINENTS

# Configurar apariencia de customtkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

"""
 * @author Yoi7
 * @date 08/11/2025
 * @description AppUI (Frontend)
"""
class ScrollableFrame(ctk.CTkFrame):
    """Frame personalizado con scrollbar global para manejar contenido extenso"""

    def __init__(self, master, **kwargs):
        # Inicializar el frame padre
        super().__init__(master, **kwargs)

        # Crear canvas y scrollbar para el desplazamiento
        self.canvas = tk.Canvas(self, bg=self._fg_color, highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color=self._fg_color)

        # Configurar el frame scrollable para ajustar su tamaño
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Crear ventana en el canvas para el frame scrollable
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Configurar el canvas para usar el scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Empaquetar elementos en la interfaz
        self.canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.scrollbar.pack(side="right", fill="y")

        # Bind events para redimensionamiento y scroll con mouse
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.scrollable_frame.bind("<Enter>", self._bind_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_mousewheel)

    def _on_canvas_configure(self, event):
        """Ajustar el ancho del frame interno cuando el canvas cambie de tamaño"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _bind_mousewheel(self, event):
        """Vincular la rueda del ratón al canvas para desplazamiento"""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        """Desvincular la rueda del ratón cuando el cursor sale del frame"""
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Manejar el evento de la rueda del ratón para desplazamiento vertical"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class WeatherAppGUI:
    """CLASE PRINCIPAL DE LA INTERFAZ GRÁFICA
    Maneja toda la interfaz de usuario de la aplicación de pronóstico climático"""

    def __init__(self, root):
        # Configuración inicial de la ventana principal
        self.root = root
        self.root.title("🌤️ Pronóstico Climático Inteligente")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        # Instancia del pronosticador de clima
        self.forecaster = WeatherForecaster()

        # Configurar colores y componentes de la interfaz
        self.setup_colors()
        self.create_scrollable_interface()
        self.create_loading_animation()
        self.center_window()

        # Estado original de los colores para restaurar después de errores
        self.original_colors = {}

    def setup_colors(self):
        """Define la paleta de colores azules para toda la aplicación"""
        self.colors = {
            "bg_dark": "#0A1929",  # Fondo oscuro principal
            "bg_medium": "#132F4C",  # Fondo medio
            "bg_light": "#1E3A5F",  # Fondo claro
            "accent_blue": "#4A90E2",  # Azul acento
            "accent_blue_dark": "#357ABD",  # Azul oscuro
            "accent_teal": "#00C896",  # Verde azulado
            "text_primary": "#E3F2FD",  # Texto primario
            "text_secondary": "#90CAF9",  # Texto secundario
            "text_muted": "#64B5F6",  # Texto atenuado
            "success": "#00C896",  # Color éxito
            "warning": "#FFB74D",  # Color advertencia
            "error": "#FF6B6B",  # Color error
            "error_light": "#FF8A8A",  # Color error claro
            "error_dark": "#CC5555"  # Color error oscuro
        }

    def create_scrollable_interface(self):
        """Crea la interfaz principal con scrollbar global"""
        # Usar el frame scrollable personalizado
        self.scrollable_main = ScrollableFrame(
            self.root,
            fg_color=self.colors["bg_dark"]
        )
        self.scrollable_main.pack(fill="both", expand=True)

        # Frame principal donde irán todos los widgets
        self.main_frame = self.scrollable_main.scrollable_frame

        # Crear todos los componentes dentro del frame scrollable
        self.create_header()
        self.create_form_section()
        self.create_results_section()
        self.create_footer()

    def create_loading_animation(self):
        """Crea elementos de animación de carga para mejorar la experiencia de usuario"""
        self.loading_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=self.colors["accent_blue"]
        )

    def center_window(self):
        """Centra la ventana en la pantalla del usuario"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_header(self):
        """Crea el encabezado animado con título y subtítulo"""
        header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", pady=(20, 10), padx=20)

        # Título principal de la aplicación
        title_label = ctk.CTkLabel(
            header_frame,
            text="🌤️ PRONÓSTICO CLIMÁTICO",
            font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title_label.pack(pady=(10, 5))

        # Subtítulo animado que cambia automáticamente
        self.subtitle_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=16),
            text_color=self.colors["text_muted"]
        )
        self.subtitle_label.pack(pady=(0, 10))

        # Iniciar animación del subtítulo
        self.animate_subtitle()

    def animate_subtitle(self):
        """Anima el texto del subtítulo con diferentes mensajes en ciclo"""
        texts = [
            "Predicciones inteligentes con Machine Learning...",
            "Tecnología avanzada para tu día a día...",
            "Precisión y confiabilidad en cada pronóstico...",
            "Analizando patrones climáticos globales..."
        ]

        def cycle_texts(index=0):
            text = texts[index]
            self.typewriter_effect(self.subtitle_label, text, 0.03)
            self.root.after(3000, lambda: cycle_texts((index + 1) % len(texts)))

        cycle_texts()

    def typewriter_effect(self, widget, text, delay):
        """Efecto máquina de escribir para animación de texto"""
        widget.configure(text="")

        def add_char(i=0):
            if i < len(text):
                current_text = widget.cget("text") + text[i]
                widget.configure(text=current_text)
                self.root.after(int(delay * 1000), lambda: add_char(i + 1))

        add_char()

    def create_form_section(self):
        """Crea la sección del formulario para ingresar ubicación"""
        form_container = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["bg_medium"],
            corner_radius=15
        )
        form_container.pack(fill="x", padx=20, pady=10, ipady=20)

        # Título del formulario
        form_title = ctk.CTkLabel(
            form_container,
            text="📍 INGRESA LA UBICACIÓN",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        form_title.pack(pady=(15, 25))

        # Contenedor para los campos del formulario
        fields_container = ctk.CTkFrame(form_container, fg_color="transparent")
        fields_container.pack(fill="x", padx=50, pady=10)

        # Campo Ciudad
        city_frame = ctk.CTkFrame(fields_container, fg_color="transparent")
        city_frame.pack(fill="x", pady=12)

        city_label = ctk.CTkLabel(
            city_frame,
            text="Ciudad:",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.colors["text_secondary"]
        )
        city_label.pack(anchor="w")

        self.city_entry = ctk.CTkEntry(
            city_frame,
            placeholder_text="Ej: Madrid, Bogotá, Nueva York...",
            height=45,
            border_color=self.colors["accent_blue"],
            fg_color=self.colors["bg_light"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(family="Segoe UI", size=14),
            corner_radius=10
        )
        self.city_entry.pack(fill="x", pady=(5, 0))
        self.city_entry.bind("<KeyRelease>", self.on_input_change)

        # Campo País
        country_frame = ctk.CTkFrame(fields_container, fg_color="transparent")
        country_frame.pack(fill="x", pady=12)

        country_label = ctk.CTkLabel(
            country_frame,
            text="País:",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.colors["text_secondary"]
        )
        country_label.pack(anchor="w")

        self.country_entry = ctk.CTkEntry(
            country_frame,
            placeholder_text="Ej: España, Colombia, Estados Unidos...",
            height=45,
            border_color=self.colors["accent_blue"],
            fg_color=self.colors["bg_light"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(family="Segoe UI", size=14),
            corner_radius=10
        )
        self.country_entry.pack(fill="x", pady=(5, 0))
        self.country_entry.bind("<KeyRelease>", self.on_input_change)

        # Campo Continente (opcional)
        continent_frame = ctk.CTkFrame(fields_container, fg_color="transparent")
        continent_frame.pack(fill="x", pady=12)

        continent_label = ctk.CTkLabel(
            continent_frame,
            text="Continente (opcional):",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.colors["text_secondary"]
        )
        continent_label.pack(anchor="w")

        self.continent_cb = ctk.CTkComboBox(
            continent_frame,
            values=CONTINENTS,
            height=45,
            border_color=self.colors["accent_blue"],
            fg_color=self.colors["bg_light"],
            button_color=self.colors["accent_blue"],
            button_hover_color=self.colors["accent_blue_dark"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(family="Segoe UI", size=14),
            state="readonly",
            corner_radius=10
        )
        self.continent_cb.set("Seleccione continente")
        self.continent_cb.pack(fill="x", pady=(5, 0))

        # Sección de botones
        button_frame = ctk.CTkFrame(fields_container, fg_color="transparent")
        button_frame.pack(fill="x", pady=25)

        # Botón principal de consulta
        self.consult_button = ctk.CTkButton(
            button_frame,
            text="🔍 CONSULTAR PRONÓSTICO",
            command=self.on_consult,
            width=200,
            height=50,
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            fg_color=self.colors["accent_blue"],
            hover_color=self.colors["accent_blue_dark"],
            corner_radius=12,
            state="disabled"  # Inicialmente deshabilitado
        )
        self.consult_button.pack(side="left", padx=(0, 15))

        # Botón para limpiar campos
        self.clear_button = ctk.CTkButton(
            button_frame,
            text="🧹 LIMPIAR",
            command=self.on_clear,
            width=120,
            height=50,
            font=ctk.CTkFont(family="Segoe UI", size=14),
            fg_color=self.colors["bg_light"],
            hover_color=self.colors["accent_blue_dark"],
            border_color=self.colors["accent_blue"],
            border_width=2,
            text_color=self.colors["text_primary"],
            corner_radius=12
        )
        self.clear_button.pack(side="left")

    def create_results_section(self):
        """Crea la sección de resultados con tabla y predicción"""
        self.results_container = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["bg_medium"],
            corner_radius=15
        )
        self.results_container.pack(fill="both", expand=True, padx=20, pady=10, ipady=20)

        # Título de la sección de resultados
        results_title = ctk.CTkLabel(
            self.results_container,
            text="📊 PROMEDIOS DE LOS ÚLTIMOS 10 DÍAS",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        results_title.pack(pady=(15, 20))

        # Contenedor para el contenido de resultados
        content_container = ctk.CTkFrame(self.results_container, fg_color="transparent")
        content_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Frame para la tabla de resultados
        table_frame = ctk.CTkFrame(
            content_container,
            fg_color=self.colors["bg_light"],
            corner_radius=10
        )
        table_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Crear Treeview con estilo personalizado para la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background=self.colors["bg_light"],
                        fieldbackground=self.colors["bg_light"],
                        foreground=self.colors["text_primary"],
                        borderwidth=0,
                        font=('Segoe UI', 11))
        style.configure("Custom.Treeview.Heading",
                        background=self.colors["accent_blue"],
                        foreground=self.colors["text_primary"],
                        font=('Segoe UI', 12, 'bold'))
        style.map('Custom.Treeview',
                  background=[('selected', self.colors["accent_blue_dark"])])

        # Frame para treeview y scrollbar
        tree_scroll_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        tree_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview - Tabla para mostrar promedios diarios
        self.tree = ttk.Treeview(
            tree_scroll_frame,
            columns=("date", "avg_temp"),
            show="headings",
            height=10,  # Altura para 10 filas
            style="Custom.Treeview"
        )

        # Configurar columnas de la tabla
        self.tree.heading("date", text="📅 FECHA")
        self.tree.heading("avg_temp", text="🌡️ TEMP. PROMEDIO (°C)")
        self.tree.column("date", width=200, anchor="center")
        self.tree.column("avg_temp", width=200, anchor="center")

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(
            tree_scroll_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Usar grid para treeview y scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configurar el peso de las columnas para que se expandan
        tree_scroll_frame.grid_rowconfigure(0, weight=1)
        tree_scroll_frame.grid_columnconfigure(0, weight=1)

        # Contenedor para la predicción actual
        prediction_container = ctk.CTkFrame(content_container, fg_color="transparent")
        prediction_container.pack(fill="x", pady=10)

        # Label para mostrar la predicción
        self.pred_label = ctk.CTkLabel(
            prediction_container,
            text="Ingresa una ubicación para ver la predicción...",
            font=ctk.CTkFont(family="Segoe UI", size=16),
            text_color=self.colors["text_muted"],
            wraplength=800
        )
        self.pred_label.pack(anchor="w")

        # Barra de progreso animada para consultas
        self.progress_bar = ctk.CTkProgressBar(
            prediction_container,
            width=500,
            height=8,
            progress_color=self.colors["accent_teal"],
            fg_color=self.colors["bg_light"],
            corner_radius=4
        )
        self.progress_bar.set(0)

    def create_footer(self):
        """Crea el pie de página con información de la aplicación"""
        footer_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        footer_frame.pack(fill="x", side="bottom", pady=20, padx=20)

        footer_label = ctk.CTkLabel(
            footer_frame,
            text="🌍 Pronóstico Climático Inteligente • Desarrollado con Python y Machine Learning • v1.0",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.colors["text_muted"]
        )
        footer_label.pack()

    def clear_table(self):
        """Limpia completamente la tabla de resultados"""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def on_input_change(self, event=None):
        """Habilita el botón cuando hay contenido en los campos obligatorios"""
        city = self.city_entry.get().strip()
        country = self.country_entry.get().strip()

        if city and country:
            self.consult_button.configure(state="normal")
            self.pulse_animation(self.consult_button)
        else:
            self.consult_button.configure(state="disabled")

    def pulse_animation(self, widget):
        """Animación de pulso para el botón cuando se habilita"""
        original_color = self.colors["accent_blue"]
        pulse_color = self.colors["accent_teal"]

        def pulse():
            widget.configure(fg_color=pulse_color)
            widget.after(200, lambda: widget.configure(fg_color=original_color))

        pulse()

    def on_clear(self):
        """Maneja la acción de limpiar todos los campos"""
        # Animación de limpieza
        self.animate_clear()

        self.root.after(500, self.perform_clear)

    def animate_clear(self):
        """Animación al limpiar campos para mejor experiencia de usuario"""
        self.clear_button.configure(
            text="✨ LIMPIANDO...",
            fg_color=self.colors["accent_teal"]
        )

        # Efecto de desvanecimiento en los campos
        widgets = [self.city_entry, self.country_entry]
        for widget in widgets:
            original_color = widget.cget("fg_color")
            widget.configure(fg_color=self.colors["bg_dark"])
            self.root.after(100, lambda w=widget, color=original_color: w.configure(fg_color=color))

    def perform_clear(self):
        """Realiza la limpieza después de la animación"""
        # Limpiar campos de entrada
        self.city_entry.delete(0, tk.END)
        self.country_entry.delete(0, tk.END)
        self.continent_cb.set("Seleccione continente")

        # Limpiar tabla de resultados
        self.clear_table()

        # Mostrar mensaje de confirmación
        self.pred_label.configure(
            text="✅ Campos limpiados • Ingresa una nueva ubicación...",
            text_color=self.colors["success"]
        )

        # Restaurar botón de limpiar
        self.clear_button.configure(
            text="🧹 LIMPIAR",
            fg_color=self.colors["bg_light"]
        )

        self.consult_button.configure(state="disabled")

        # Restaurar mensaje predeterminado después de 2 segundos
        self.root.after(2000, lambda: self.pred_label.configure(
            text="Ingresa una ubicación para ver la predicción...",
            text_color=self.colors["text_muted"]
        ))

    def on_consult(self):
        """Maneja la consulta del pronóstico - MÉTODO PRINCIPAL"""
        city = self.city_entry.get().strip()
        country = self.country_entry.get().strip()
        continent = self.continent_cb.get()

        # Validar campos obligatorios
        if not city or not country:
            self.show_error_message("❌ Por favor ingresa al menos ciudad y país", is_validation_error=True)
            return

        if continent == "Seleccione continente":
            continent = None

        # Limpiar tabla inmediatamente al iniciar consulta
        self.clear_table()

        # Deshabilitar interfaz durante la consulta
        self.consult_button.configure(state="disabled", text="⏳ CONSULTANDO...")
        self.progress_bar.pack(pady=15)

        # Mostrar animación de carga
        self.show_loading_animation()

        # Guardar colores originales antes de posible error
        self.save_original_colors()

        # Ejecutar en hilo separado para no bloquear la interfaz
        threading.Thread(
            target=self.run_weather_workflow,
            args=(city, country, continent),
            daemon=True
        ).start()

    def save_original_colors(self):
        """Guarda los colores originales para restaurarlos después de errores"""
        self.original_colors = {
            "city_border": self.city_entry.cget("border_color"),
            "country_border": self.country_entry.cget("border_color"),
            "continent_border": self.continent_cb.cget("border_color"),
            "form_bg": self.results_container.cget("fg_color")
        }

    def show_loading_animation(self):
        """Muestra animación de carga durante la consulta"""
        self.progress_bar.set(0)
        loading_steps = ["🌤️ Analizando ubicación", "📡 Conectando con satélites", "🤖 Procesando datos",
                         "📊 Generando predicción"]

        def update_loading(step=0):
            if step < len(loading_steps):
                self.pred_label.configure(
                    text=loading_steps[step],
                    text_color=self.colors["accent_blue"]
                )
                self.progress_bar.set((step + 1) / len(loading_steps))
                self.root.after(800, lambda: update_loading(step + 1))

        update_loading()

    def run_weather_workflow(self, city, country, continent):
        """Ejecuta el flujo de trabajo del clima en hilo separado"""
        try:
            # Obtener predicción del servicio
            result = self.forecaster.get_weather_prediction(city, country, continent)

            if result["success"]:
                # Mostrar resultados exitosos en el hilo principal
                self.root.after(0, self.display_success_results, result)
            else:
                # Mostrar error en el hilo principal
                self.root.after(0, self.display_error, result["error"])

        except Exception as e:
            self.root.after(0, self.display_error, str(e))

    def display_success_results(self, result):
        """Muestra los resultados exitosos con mensaje de éxito"""
        # Ocultar barra de progreso
        self.progress_bar.pack_forget()

        # Mostrar mensaje de éxito animado
        self.show_success_animation(result["city"], result["country"])

        # Llenar tabla con promedios diarios
        daily_averages = result["daily_averages"]
        for date, avg_temp in daily_averages:
            # Formatear fecha de YYYY-MM-DD a DD/MM/YYYY
            formatted_date = self.format_date(date)
            self.tree.insert("", tk.END, values=(formatted_date, f"{avg_temp:.2f}°C"))

        # Mostrar predicción con animación
        lat, lon = result["coordinates"]
        pred = result["prediction"]

        prediction_text = f"✅ PREDICCIÓN PARA HOY: {pred:.2f}°C • 📍 Coordenadas: {lat:.4f}, {lon:.4f}"

        # Animación de texto de predicción
        self.root.after(2500, lambda: self.animate_prediction_text(prediction_text))

        # Restaurar botón de consulta
        self.consult_button.configure(state="normal", text="🔍 CONSULTAR PRONÓSTICO")

    def format_date(self, date_str):
        """Formatea la fecha de YYYY-MM-DD a DD/MM/YYYY"""
        try:
            year, month, day = date_str.split('-')
            return f"{day}/{month}/{year}"
        except:
            return date_str

    def show_success_animation(self, city, country):
        """Muestra animación de éxito al consultar"""
        success_messages = [
            f"✅ ¡Consulta exitosa para {city}, {country}!",
            "📊 Calculando promedios diarios...",
            "🌡️ Analizando patrones climáticos...",
            "🎯 Predicción generada con éxito!"
        ]

        def show_message(index=0):
            if index < len(success_messages):
                self.pred_label.configure(
                    text=success_messages[index],
                    text_color=self.colors["success"]
                )
                # Efecto de pulso en el texto de éxito
                self.pulse_text_animation(self.pred_label)
                self.root.after(600, lambda: show_message(index + 1))

        show_message()

    def pulse_text_animation(self, widget):
        """Animación de pulso para el texto"""
        original_size = 16
        pulse_size = 18

        def pulse():
            widget.configure(font=ctk.CTkFont(family="Segoe UI", size=pulse_size, weight="bold"))
            widget.after(200, lambda: widget.configure(
                font=ctk.CTkFont(family="Segoe UI", size=original_size, weight="bold")
            ))

        pulse()

    def animate_prediction_text(self, text):
        """Anima el texto de predicción con efecto máquina de escribir"""
        self.pred_label.configure(text="", text_color=self.colors["success"])

        def type_text(i=0):
            if i < len(text):
                current_text = self.pred_label.cget("text") + text[i]
                self.pred_label.configure(text=current_text)
                self.root.after(30, lambda: type_text(i + 1))

        type_text()

    def display_error(self, error_msg):
        """Muestra mensaje de error con efectos visuales"""
        self.progress_bar.pack_forget()
        self.consult_button.configure(state="normal", text="🔍 CONSULTAR PRONÓSTICO")

        # Aplicar efecto de error visual
        self.apply_error_visuals()

        # Mostrar mensaje de error con animación
        self.show_detailed_error_message(error_msg)

        # Programar restauración de colores
        self.root.after(3000, self.restore_original_colors)

    def apply_error_visuals(self):
        """Aplica efectos visuales de error en la interfaz"""
        # Cambiar colores a tonos rojos
        error_color = self.colors["error"]
        error_bg = self.colors["error_dark"]

        self.city_entry.configure(border_color=error_color)
        self.country_entry.configure(border_color=error_color)
        self.continent_cb.configure(border_color=error_color)

        # Efecto de parpadeo suave en el formulario
        self.flash_error_effect()

    def flash_error_effect(self):
        """Efecto de parpadeo suave para indicar error"""
        original_color = self.colors["bg_medium"]
        error_color = "#552222"  # Rojo oscuro suave

        def flash(count=0):
            if count < 6:  # 3 parpadeos completos
                if count % 2 == 0:
                    self.results_container.configure(fg_color=error_color)
                else:
                    self.results_container.configure(fg_color=original_color)
                self.root.after(150, lambda: flash(count + 1))
            else:
                self.results_container.configure(fg_color=original_color)

        flash()

    def restore_original_colors(self):
        """Restaura los colores originales después de un error"""
        if self.original_colors:
            self.city_entry.configure(border_color=self.original_colors["city_border"])
            self.country_entry.configure(border_color=self.original_colors["country_border"])
            self.continent_cb.configure(border_color=self.original_colors["continent_border"])
            self.results_container.configure(fg_color=self.original_colors["form_bg"])

    def show_detailed_error_message(self, error_msg):
        """Muestra un mensaje de error detallado y notable en ventana emergente"""
        # Crear ventana de error emergente
        error_window = ctk.CTkToplevel(self.root)
        error_window.title("❌ Error en la Consulta")
        error_window.geometry("500x300")
        error_window.resizable(False, False)
        error_window.transient(self.root)
        error_window.grab_set()

        # Centrar ventana de error
        error_window.update_idletasks()
        x = (self.root.winfo_x() + self.root.winfo_width() // 2) - 250
        y = (self.root.winfo_y() + self.root.winfo_height() // 2) - 150
        error_window.geometry(f"500x300+{x}+{y}")

        # Configurar estilo de la ventana de error
        error_window.configure(fg_color=self.colors["error_dark"])

        # Contenido de la ventana de error
        error_container = ctk.CTkFrame(error_window, fg_color=self.colors["error_dark"])
        error_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Icono de error
        error_icon = ctk.CTkLabel(
            error_container,
            text="⚠️",
            font=ctk.CTkFont(family="Segoe UI", size=48),
            text_color=self.colors["error_light"]
        )
        error_icon.pack(pady=(10, 20))

        # Título del error
        error_title = ctk.CTkLabel(
            error_container,
            text="ERROR EN LA CONSULTA",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        error_title.pack(pady=(0, 10))

        # Mensaje de error detallado
        error_message = ctk.CTkLabel(
            error_container,
            text=error_msg,
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color=self.colors["text_primary"],
            wraplength=400
        )
        error_message.pack(pady=(0, 20))

        # Sugerencias para el usuario
        suggestions = ctk.CTkLabel(
            error_container,
            text="💡 Sugerencias:\n• Verifica la ortografía de ciudad y país\n• Intenta ser más específico\n• Revisa tu conexión a internet",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.colors["text_secondary"],
            justify="left"
        )
        suggestions.pack(pady=(0, 20))

        # Botón para cerrar la ventana de error
        close_button = ctk.CTkButton(
            error_container,
            text="ENTENDIDO",
            command=error_window.destroy,
            width=120,
            height=40,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=self.colors["error"],
            hover_color=self.colors["error_light"],
            corner_radius=10
        )
        close_button.pack(pady=10)

        # También mostrar el error en la etiqueta principal
        self.pred_label.configure(
            text=f"❌ Error: {error_msg}",
            text_color=self.colors["error"]
        )

    def show_error_message(self, message, is_validation_error=False):
        """Muestra mensaje de error con animación de parpadeo"""
        original_color = self.pred_label.cget("text_color")
        self.pred_label.configure(text=message, text_color=self.colors["error"])

        if is_validation_error:
            self.save_original_colors()
            self.apply_error_visuals()
            self.root.after(3000, self.restore_original_colors)

        def blink(count=0):
            if count < 6:  # 3 parpadeos
                if count % 2 == 0:
                    self.pred_label.configure(text_color=self.colors["error"])
                else:
                    self.pred_label.configure(text_color=original_color)
                self.root.after(200, lambda: blink(count + 1))

        blink()
