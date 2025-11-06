<<<<<<< HEAD
# GPS MQTT Dashboard (Simulador de Rastreo)

Proyecto sencillo para **simular vehículos** publicando posiciones **GPS** por **MQTT** y visualizar en un **dashboard web** con **Leaflet** en tiempo real.

## 🚀 Características
- Publica telemetría GPS simulada de N vehículos con `simulator/simulator.py`.
- **Broker MQTT Mosquitto** vía `docker-compose` (puerto 1883).
- **Dashboard Node.js**: suscribe a MQTT y retransmite a WebSocket, visualizando en un mapa.
- Tópicos por vehículo: `fleet/<vehiculo_id>/telemetry`.
- Sin hardware: todo corre local.

## 📦 Requisitos
- Docker + Docker Compose (para el broker).
- Node.js 18+ (para el dashboard).
- Python 3.9+ (para el simulador).

## 🧩 Arquitectura
```
Simulador (Python) → MQTT (Mosquitto) → Dashboard (Node.js + Socket.IO) → Navegador (Leaflet)
```
- Mensaje JSON de telemetría:
```json
{
  "id": "vehiculo-1",
  "lat": 14.6349,
  "lon": -90.5069,
  "speed_kmh": 35.2,
  "bearing_deg": 120.0,
  "ts": 1730419200
}
```

## 🛠️ Instalación rápida

1) Clonar o extraer este repo.
2) **Broker MQTT** (Docker):
```bash
docker compose up -d
```
- Esto levanta Mosquitto en `localhost:1883` (anónimo habilitado).

3) **Dashboard**:
```bash
cd dashboard
npm install
npm start
```
- Abre: http://localhost:3000

4) **Simulador** (en otra terminal):
```bash
cd simulator
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Ejemplo: 3 vehículos, mensaje cada 1.0 s, alrededor de zona 10 GUA
python simulator.py --vehicles 3 --interval 1.0 --center-lat 14.591 --center-lon -90.516 --radius-m 1200
```
- También puedes usar variables de entorno (ver `.env.example`).

## ⚙️ Variables de entorno
Copia `.env.example` a `.env` y ajusta si lo deseas. Valores por defecto ya funcionan localmente.

- `MQTT_HOST=localhost`
- `MQTT_PORT=1883`
- `MQTT_TOPIC_BASE=fleet`
- `DASHBOARD_PORT=3000`

## 🧪 Pruebas rápidas MQTT
Publica manualmente:
```bash
# Linux/macOS (mosquitto-clients)
mosquitto_pub -h localhost -t fleet/test/telemetry -m '{"id":"test","lat":14.6,"lon":-90.5,"speed_kmh":10,"bearing_deg":0,"ts":1759370954}'
```

## 📝 Notas
- El dashboard traza la última posición y la ruta de cada vehículo.
- Para producción, deshabilita `allow_anonymous` y configura usuarios en Mosquitto.

## 📚 Justificación académica (Fase 1)
- **Contexto del problema**: PyMEs de logística necesitan monitoreo básico de su flota en tiempo real sin invertir en hardware.
- **Objetivos**:
  1. Simular transmisión de coordenadas GPS en tiempo real para múltiples vehículos.
  2. Diseñar arquitectura telemática basada en **MQTT** para transporte eficiente de datos.
  3. Visualizar posiciones y trayectorias en un dashboard web, con actualización en vivo.
- **Arquitectura preliminar**: ver diagrama ASCII superior y módulos: simulador (productor), broker (transporte), backend/dashboard (consumidor y visualizador).

---

© 2025 – Proyecto educativo.
=======

>>>>>>> 0b54c1d2932913a6b5fa7ed09e9dfad6569190aa
