import os, time, json, math, random, argparse
from datetime import datetime
import paho.mqtt.client as mqtt

def haversine_point(lat, lon, bearing_deg, distance_m):
    R = 6371000.0
    br = math.radians(bearing_deg)
    lat1 = math.radians(lat)
    lon1 = math.radians(lon)
    lat2 = math.asin(math.sin(lat1)*math.sin(distance_m/R) + math.cos(lat1)*math.cos(distance_m/R)*math.cos(br))
    lon2 = lon1 + math.atan2(math.sin(br)*math.sin(distance_m/R)*math.cos(lat1),
                             math.cos(distance_m/R)-math.sin(lat1)*math.sin(lat2))
    return math.degrees(lat2), math.degrees(lon2)

def main():
    parser = argparse.ArgumentParser(description="Simulador de vehículos publicando GPS por MQTT.")
    parser.add_argument("--vehicles", type=int, default=int(os.getenv("VEHICLES", "3")), help="Cantidad de vehículos a simular")
    parser.add_argument("--interval", type=float, default=float(os.getenv("INTERVAL", "1.0")), help="Intervalo entre mensajes (s)")
    parser.add_argument("--center-lat", type=float, default=float(os.getenv("CENTER_LAT", "14.6349")), help="Centro latitud")
    parser.add_argument("--center-lon", type=float, default=float(os.getenv("CENTER_LON", "-90.5069")), help="Centro longitud")
    parser.add_argument("--radius-m", type=float, default=float(os.getenv("RADIUS_M", "1000")), help="Radio de circuito (m)")
    parser.add_argument("--mqtt-host", type=str, default=os.getenv("MQTT_HOST", "localhost"))
    parser.add_argument("--mqtt-port", type=int, default=int(os.getenv("MQTT_PORT", "1883")))
    parser.add_argument("--topic-base", type=str, default=os.getenv("MQTT_TOPIC_BASE", "fleet"))
    args = parser.parse_args()

    client = mqtt.Client()
    client.connect(args.mqtt_host, args.mqtt_port, keepalive=60)
    client.loop_start()

    # Estado inicial por vehículo
    states = []
    for i in range(args.vehicles):
        bearing = random.uniform(0, 360)
        speed = random.uniform(20, 50)  # km/h
        # posicion inicial en el perímetro del círculo
        lat0, lon0 = haversine_point(args.center_lat, args.center_lon, bearing, args.radius_m)
        states.append({
            "id": f"vehiculo-{i+1}",
            "lat": lat0,
            "lon": lon0,
            "speed_kmh": speed,
            "bearing_deg": bearing
        })

    print(f"[SIM] Publicando en MQTT mqtt://{args.mqtt_host}:{args.mqtt_port} base '{args.topic_base}/<id>/telemetry'")
    try:
        while True:
            for s in states:
                # mover un pequeño tramo según velocidad
                # velocidad (km/h) -> m/s
                ms = s["speed_kmh"] * 1000 / 3600.0
                # distancia en el intervalo
                dist = ms * args.interval
                # variación leve de rumbo y velocidad
                s["bearing_deg"] += random.uniform(-5, 5)
                s["speed_kmh"] = max(5, min(70, s["speed_kmh"] + random.uniform(-2, 2)))
                new_lat, new_lon = haversine_point(s["lat"], s["lon"], s["bearing_deg"], dist)
                s["lat"], s["lon"] = new_lat, new_lon

                payload = {
                    "id": s["id"],
                    "lat": s["lat"],
                    "lon": s["lon"],
                    "speed_kmh": round(s["speed_kmh"], 1),
                    "bearing_deg": round(s["bearing_deg"] % 360, 1),
                    "ts": int(datetime.utcnow().timestamp())
                }
                topic = f"{args.topic_base}/{s['id']}/telemetry"
                client.publish(topic, json.dumps(payload), qos=0, retain=False)
                print(f"[PUB] {topic} -> {payload}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
