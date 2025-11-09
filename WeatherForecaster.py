import datetime
import requests
import numpy as np
from sklearn.linear_model import LinearRegression
from collections import defaultdict

# ── CONSTANTES GLOBALES ─────────────────────────────────────────────────────
HISTORICAL_DAYS = 30  # Días de datos históricos para entrenar el modelo
OPEN_METEO_HIST_URL = "https://archive-api.open-meteo.com/v1/archive"  # API datos históricos
OPEN_METEO_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"  # API geocodificación
VARIABLES = ["temperature_2m"]  # Variables climáticas a obtener

# Lista de continentes para el combobox
CONTINENTS = ["África", "América del Norte", "América del Sur", "Asia", "Europa", "Oceanía", "Antártica"]


class WeatherForecaster:
    """CLASE PRINCIPAL DEL PRONOSTICADOR CLIMÁTICO
    Maneja toda la lógica de obtención de datos y predicciones"""

    def __init__(self):
        # Inicialización simple - se podrían agregar configuraciones aquí
        pass

    @staticmethod
    def resolve_coords_by_name(city: str, country: str, continent: str = None):
        """CONVERTIR NOMBRE DE UBICACIÓN A COORDENADAS GEOGRÁFICAS
        Usa la API de geocodificación para obtener latitud y longitud"""
        # Construir query de búsqueda
        query = f"{city}, {country}"
        if continent:
            query += f", {continent}"

        # Parámetros para la API de geocodificación
        params = {
            "name": query,
            "count": 1,  # Solo el primer resultado
            "language": "es"  # Idioma español
        }

        # Realizar petición a la API
        resp = requests.get(OPEN_METEO_GEOCODE_URL, params=params, timeout=10)
        resp.raise_for_status()  # Lanzar excepción si hay error HTTP

        # Procesar respuesta
        data = resp.json()
        results = data.get("results")
        if not results:
            raise ValueError(f"No se encontró ubicación para: {query}")

        # Extraer coordenadas del primer resultado
        r = results[0]
        lat = r["latitude"]
        lon = r["longitude"]
        return lat, lon

    @staticmethod
    def fetch_historical(lat: float, lon: float, days: int = HISTORICAL_DAYS):
        """OBTENER DATOS CLIMÁTICOS HISTÓRICOS
        Recupera datos de temperatura de los últimos 'days' días"""
        # Calcular fechas de inicio y fin
        end = datetime.date.today()
        start = end - datetime.timedelta(days=days)

        # Parámetros para la API de datos históricos
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "hourly": ",".join(VARIABLES),
            "timezone": "auto"  # Zona horaria automática
        }

        # Realizar petición a la API
        resp = requests.get(OPEN_METEO_HIST_URL, params=params, timeout=10)
        resp.raise_for_status()

        # Procesar y retornar datos
        data = resp.json()
        if "hourly" not in data:
            raise ValueError("Respuesta inesperada de la API: no contiene datos 'hourly'")
        return data["hourly"]

    @staticmethod
    def preprocess_hourly(hourly: dict):
        """PREPROCESAR DATOS HORARIOS PARA EL MODELO
        Convierte datos temporales en características numéricas"""
        # Extraer listas de tiempos y temperaturas
        times = hourly["time"]
        temps = hourly["temperature_2m"]

        # Calcular tiempo base para referencia
        base = datetime.datetime.fromisoformat(times[0])

        # Preparar arrays para el modelo
        X = []  # Características (horas desde base)
        y = []  # Objetivo (temperaturas)

        # Convertir cada timestamp a horas desde el tiempo base
        for t_str, temp in zip(times, temps):
            dt = datetime.datetime.fromisoformat(t_str)
            hours = (dt - base).total_seconds() / 3600.0  # Convertir segundos a horas
            X.append([hours])
            y.append(temp)

        return np.array(X), np.array(y), base, times, temps

    @staticmethod
    def train_simple_model(X: np.ndarray, y: np.ndarray):
        """ENTRENAR MODELO DE REGRESIÓN LINEAL
        Crea y entrena un modelo simple para predecir temperatura"""
        model = LinearRegression()
        model.fit(X, y)  # Entrenar con datos históricos
        return model

    @staticmethod
    def predict_today(model, base: datetime.datetime):
        """REALIZAR PREDICCIÓN PARA EL DÍA ACTUAL
        Usa el modelo entrenado para predecir temperatura actual"""
        # Calcular horas desde el tiempo base hasta ahora
        now = datetime.datetime.now()
        hours = (now - base).total_seconds() / 3600.0

        # Realizar predicción
        pred = model.predict(np.array([[hours]]))[0]
        return pred

    def calculate_daily_averages(self, times: list, temps: list, days: int = 10):
        """CALCULAR PROMEDIOS DIARIOS DE TEMPERATURA
        Agrupa temperaturas horarias en promedios diarios"""
        daily_data = defaultdict(list)

        # Agrupar temperaturas por día
        for time_str, temp in zip(times, temps):
            if temp is not None:  # Solo si hay temperatura válida
                date = time_str.split('T')[0]  # Extraer solo la fecha (YYYY-MM-DD)
                daily_data[date].append(temp)

        # Calcular promedios diarios
        daily_averages = []
        for date, day_temps in daily_data.items():
            if day_temps:  # Si hay temperaturas para ese día
                avg_temp = sum(day_temps) / len(day_temps)
                daily_averages.append((date, avg_temp))

        # Ordenar por fecha y tomar los últimos 'days' días
        daily_averages.sort(key=lambda x: x[0])
        last_10_days = daily_averages[-days:]

        return last_10_days

    def get_weather_prediction(self, city: str, country: str, continent: str = None):
        """MÉTODO PRINCIPAL - OBTENER PREDICCIÓN CLIMÁTICA COMPLETA
        Orquesta todo el proceso de geocodificación, obtención de datos y predicción"""
        try:
            # 1. OBTENER COORDENADAS GEOGRÁFICAS
            lat, lon = self.resolve_coords_by_name(city, country, continent)

            # 2. OBTENER DATOS HISTÓRICOS
            hourly = self.fetch_historical(lat, lon, HISTORICAL_DAYS)

            # 3. PREPROCESAR DATOS
            X, y, base, times, temps = self.preprocess_hourly(hourly)

            # 4. CALCULAR PROMEDIOS DIARIOS (últimos 10 días)
            daily_averages = self.calculate_daily_averages(times, temps, days=10)

            # 5. ENTRENAR MODELO DE MACHINE LEARNING
            model = self.train_simple_model(X, y)

            # 6. REALIZAR PREDICCIÓN PARA HOY
            pred = self.predict_today(model, base)

            # Retornar resultados completos
            return {
                "success": True,
                "daily_averages": daily_averages,  # Promedios de últimos 10 días
                "prediction": pred,  # Predicción para hoy
                "coordinates": (lat, lon),  # Coordenadas de la ubicación
                "city": city,  # Ciudad consultada
                "country": country  # País consultado
            }

        except Exception as e:
            # Retornar error en caso de fallo
            return {
                "success": False,
                "error": str(e)  # Mensaje de error descriptivo
            }