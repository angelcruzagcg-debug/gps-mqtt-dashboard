const map = L.map("map").setView([14.6349, -90.5069], 12);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
}).addTo(map);

const socket = io();
const markers = new Map();
const polylines = new Map();

function upsertLegend(id, speed, bearing) {
  const ul = document.getElementById("legend-list");
  let li = document.getElementById(`legend-${id}`);
  if (!li) {
    li = document.createElement("li");
    li.id = `legend-${id}`;
    ul.appendChild(li);
  }
  li.innerHTML = `<strong>${id}</strong> <span class="badge">${speed ?? "-"} km/h</span> <span class="badge">⮕ ${bearing ?? "-" }°</span>`;
}

socket.on("telemetry", ({ id, data, trail }) => {
  const { lat, lon, speed_kmh, bearing_deg } = data;

  // marker
  let m = markers.get(id);
  if (!m) {
    const icon = L.divIcon({
      className: "veh-icon",
      html: `<div style="transform: rotate(${bearing_deg || 0}deg);">🚚</div>`,
      iconSize: [24, 24],
      iconAnchor: [12, 12]
    });
    m = L.marker([lat, lon], { icon }).addTo(map).bindPopup(id);
    markers.set(id, m);
  } else {
    m.setLatLng([lat, lon]);
    // rotate emoji by updating HTML
    const el = m.getElement();
    if (el) el.innerHTML = `<div style="transform: rotate(${bearing_deg || 0}deg);">🚚</div>`;
  }

  // polyline
  let pl = polylines.get(id);
  if (!pl) {
    pl = L.polyline(trail.map(p => [p.lat, p.lon])).addTo(map);
    polylines.set(id, pl);
  } else {
    pl.setLatLngs(trail.map(p => [p.lat, p.lon]));
  }

  upsertLegend(id, speed_kmh, bearing_deg);
});
