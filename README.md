# 🌤️ ClimaPredictor-ML - Sistema Inteligente de Pronóstico Climático

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange)](https://scikit-learn.org)
[![GUI](https://img.shields.io/badge/GUI-CustomTkinter-green)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**Aplicación de escritorio inteligente que utiliza Machine Learning para generar predicciones climáticas precisas en tiempo real.**

<div align="center">

*Interfaz moderna y oscura del sistema*

</div>

## 🚀 Características Principales

### 🔍 **Geolocalización Inteligente**
- ✅ Búsqueda avanzada por ciudad, país y continente
- ✅ Geocodificación automática con Open-Meteo API
- ✅ Validación en tiempo real de ubicaciones
- ✅ Coordenadas precisas con tolerancia a errores ortográficos

### 🤖 **Machine Learning Integrado**
- ✅ Modelo de regresión lineal con Scikit-learn
- ✅ Entrenamiento con datos históricos de 30 días
- ✅ Predicciones en tiempo real para la temperatura actual
- ✅ Análisis automático de patrones climáticos

### 💻 **Interfaz Moderna y Responsive**
- ✅ Diseño oscuro con CustomTkinter
- ✅ Animaciones fluidas y efectos visuales
- ✅ Tabla interactiva con scroll para resultados
- ✅ Barra de progreso animada durante consultas
- ✅ Manejo elegante de errores con ventanas emergentes

### 📊 **Visualización de Datos Avanzada**
- ✅ Promedios diarios de temperatura últimos 10 días
- ✅ Predicción en tiempo real para el día actual
- ✅ Formato de fechas internacional (DD/MM/YYYY)
- ✅ Coordenadas geográficas con alta precisión

## 🛠️ Tecnologías Utilizadas

| Categoría | Tecnologías |
|-----------|-------------|
| **Lenguaje** | Python 3.8+ |
| **Interfaz Gráfica** | CustomTkinter, Tkinter, ttk |
| **Machine Learning** | Scikit-learn, NumPy |
| **APIs Externas** | Open-Meteo (Clima + Geocodificación) |
| **Concurrencia** | Threading |
| **Procesamiento** | Collections, DateTime, Requests |

## 📦 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- Conexión a Internet
- 100MB de espacio libre

### Método 1: Instalación Rápida
```bash
# Clonar el repositorio
git clone https://github.com/Y0i7/WeatherForecast-AI.git
cd WeatherForecast-AI

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py
