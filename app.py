import customtkinter as ctk

from AppUI import WeatherAppGUI

"""
 * @author Yoi
 * @date 2025/04/18
 * @description DeliveryMapper.java
"""


def main():
    """
    FUNCIÓN PRINCIPAL DE LA APLICACIÓN
    Punto de entrada de la aplicación de pronóstico climático
    """
    # Configurar apariencia visual de la aplicación
    ctk.set_appearance_mode("Dark")  # Modo oscuro
    ctk.set_default_color_theme("blue")  # Tema de colores azul

    # Crear ventana principal de la aplicación
    root = ctk.CTk()

    # Configurar el color de fondo de la ventana
    root.configure(fg_color="#0A1929")  # Color de fondo coherente

    # Inicializar la interfaz gráfica de la aplicación
    app = WeatherAppGUI(root)

    # Iniciar el bucle principal de la aplicación
    root.mainloop()


if __name__ == "__main__":
    # Ejecutar la aplicación cuando el script se ejecute directamente
    main()
