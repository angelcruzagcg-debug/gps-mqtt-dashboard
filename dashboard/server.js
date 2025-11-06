import express from "express";
import { createServer } from "http";
import { Server as SocketIOServer } from "socket.io";
import mqtt from "mqtt";
import dotenv from "dotenv";
dotenv.config();

const PORT = process.env.DASHBOARD_PORT || 3000;
const MQTT_HOST = process.env.MQTT_HOST || "localhost";
const MQTT_PORT = process.env.MQTT_PORT || 1883;
const MQTT_TOPIC_BASE = process.env.MQTT_TOPIC_BASE || "fleet";

const app = express();
const httpServer = createServer(app);
const io = new SocketIOServer(httpServer, { cors: { origin: "*" } });

app.use(express.static("public"));

const url = `mqtt://${MQTT_HOST}:${MQTT_PORT}`;
console.log(`[MQTT] Connecting to ${url}`);
const client = mqtt.connect(url);

const lastPositions = new Map(); // id -> {lat, lon, speed_kmh, bearing_deg, ts}
const trails = new Map(); // id -> [{lat, lon}]

client.on("connect", () => {
  console.log("[MQTT] Connected");
  client.subscribe(`${MQTT_TOPIC_BASE}/+/telemetry`);
});

client.on("message", (topic, payload) => {
  try {
    const data = JSON.parse(payload.toString());
    const vid = data.id || topic.split("/")[1];
    lastPositions.set(vid, data);
    if (!trails.has(vid)) trails.set(vid, []);
    const tr = trails.get(vid);
    tr.push({ lat: data.lat, lon: data.lon });
    if (tr.length > 200) tr.shift(); // limitar memoria
    io.emit("telemetry", { id: vid, data, trail: tr });
  } catch (e) {
    console.error("[MQTT] Parse error:", e);
  }
});

io.on("connection", (socket) => {
  console.log("[WS] client connected");
  // enviar estado inicial
  for (const [id, data] of lastPositions.entries()) {
    socket.emit("telemetry", { id, data, trail: trails.get(id) || [] });
  }
});

httpServer.listen(PORT, () => {
  console.log(`[HTTP] Dashboard on http://localhost:${PORT}`);
});
