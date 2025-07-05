# Calcula la distancia y duración de viaje entre una ciudad de Chile y una ciudad de Perú
import sys
import math
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Velocidades promedio en km/h para distintos medios
VELOCIDADES = {
    "coche": 100,
    "bus": 80,
    "avión": 800
}

def calcular_duracion(dist_km: float, velocidad_kmh: float):
    horas = dist_km / velocidad_kmh
    h = int(horas)
    m = int((horas - h) * 60)
    return h, m

def main():
    geolocator = Nominatim(user_agent="distancia_app")

    while True:
        origen = input("Ciudad de Origen (o 's' para salir): ").strip()
        if origen.lower() == 's':
            break

        destino = input("Ciudad de Destino (o 's' para salir): ").strip()
        if destino.lower() == 's':
            break

        print("Medios disponibles: coche, bus, avión")
        medio = input("Elige medio de transporte (o 's' para salir): ").strip().lower()
        if medio == 's':
            break
        if medio not in VELOCIDADES:
            print(f"Medio '{medio}' no reconocido. Elige uno de: {', '.join(VELOCIDADES)}.")
            continue

        # Geocodificar
        loc1 = geolocator.geocode(f"{origen}, Chile")
        loc2 = geolocator.geocode(f"{destino}, Perú")
        if not loc1 or not loc2:
            print("No pude encontrar una o ambas ciudades. Intenta nuevamente.")
            continue

        coord1 = (loc1.latitude, loc1.longitude)
        coord2 = (loc2.latitude, loc2.longitude)

        # Calcular distancias
        dist_km = geodesic(coord1, coord2).kilometers
        dist_mi = geodesic(coord1, coord2).miles

        # Calcular duración
        velocidad = VELOCIDADES[medio]
        h, m = calcular_duracion(dist_km, velocidad)

        # Mostrar resultados
        print("\n=== Resultado de la búsqueda ===")
        print(f"Viaje: {origen.title()} → {destino.title()}")
        print(f"Distancia: {dist_km:.2f} km ({dist_mi:.2f} millas)")
        print(f"Medio de transporte: {medio.capitalize()}")
        print(f"Duración estimada: {h} h {m} min")
        print(f"Narrativa: Saldrás de {origen.title()} en {medio}, recorrerás unos {dist_km:.1f} km y llegarás a {destino.title()} en aproximadamente {h} horas y {m} minutos.\n")

if __name__ == "__main__":
    main()
