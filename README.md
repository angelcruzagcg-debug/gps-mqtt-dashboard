Instructivo

1. Abrir el dashboard

Abrir CMD.

Ve a la carpeta del dashboard:

cd C:\Users\angel\Documents\telematica\gps-mqtt-dashboard\dashboard


Arrancar el dashboard:

npm start


Espera el mensaje:

[MQTT] Connecting to mqtt://broker.emqx.io:1883
[MQTT] Connected
[HTTP] Dashboard on http://localhost:3000


Dejar corriendo y no cerrar esa ventana.
En el navegador, abrir: http://localhost:3000

2. Iniciar el simulador

Abrir Anaconda Prompt.

Activar el entorno conda:

conda activate gps-sim


Ir a la carpeta del simulador:

cd C:\Users\angel\Documents\telematica\gps-mqtt-dashboard\simulator


Lanzar el simulador (ejemplo 3 vehículos):

python simulator.py --vehicles 3 --interval 1.0 --center-lat 14.591 --center-lon -90.516 --radius-m 1200 --mqtt-host broker.emqx.io --mqtt-port 1883 --topic-base fleet

3. Ver los vehículos

Volver a la pestaña del navegador en http://localhost:3000

Los vehículos aparecerán moviéndose en tiempo real.
