import network
import socket
import time
import dht
from machine import Pin

# Configuración WiFi
SSID = "HOLA"
PASSWORD = "12345678"

# Nombre para intentar que aparezca en Fing (no garantizado en AP de MicroPython)
HOSTNAME = "SFARFAN"

# Sensor DHT11 en GPIO14
sensor = dht.DHT11(Pin(14))

# Conectar a la red del ESP32 principal
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.config(dhcp_hostname=HOSTNAME)  # Intento de nombre
sta.connect(SSID, PASSWORD)

print("🔌 Conectando al AP...")
while not sta.isconnected():
    time.sleep(1)
print("✅ Conectado al AP")
print("IP asignada:", sta.ifconfig()[0])
print("Hostname (intento):", HOSTNAME)
print("📡 Enviando datos del sensor cada 5 segundos...\n")

# Enviar datos al ESP32 principal
def send_sensor_data():
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        mensaje = f"T:{temp}°C H:{hum}%"
        
        # Conectar al servidor del principal
        s = socket.socket()
        s.settimeout(3)
        s.connect(('192.168.4.1', 8888))  # IP del AP
        s.send(mensaje.encode())
        s.close()
        print(f"📤 Enviado: {mensaje}")
        return True
    except Exception as e:
        print("❌ Error al enviar datos:", e)
        return False

# Bucle principal
while True:
    send_sensor_data()
    time.sleep(5)
