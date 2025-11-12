import network
import socket
import time
import dht
from machine import Pin

# Configuración del sensor DHT11
sensor_dht = dht.DHT11(Pin(4))

# LEDs de semáforo
led_rojo = Pin(16, Pin.OUT)
led_amarillo = Pin(17, Pin.OUT)
led_verde = Pin(18, Pin.OUT)

# Configuración de red
ssid = "redes"
password = "12345678"

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Configurar IP estática para cada nodo (cambiar según el nodo)
    if NODO_ID == "sensor1":
        wlan.ifconfig(('192.168.4.10', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
    elif NODO_ID == "sensor2":
        wlan.ifconfig(('192.168.4.11', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
    elif NODO_ID == "sensor3":
        wlan.ifconfig(('192.168.4.12', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
    elif NODO_ID == "sensor4":
        wlan.ifconfig(('192.168.4.13', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
    elif NODO_ID == "sensor5":
        wlan.ifconfig(('192.168.4.14', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
    elif NODO_ID == "sensor6":
        wlan.ifconfig(('192.168.4.15', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
    elif NODO_ID == "sensor7":
        wlan.ifconfig(('192.168.4.16', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
    elif NODO_ID == "sensor8":
        wlan.ifconfig(('192.168.4.17', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
    
    if not wlan.isconnected():
        print(f"Conectando a la red con IP estática...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(1)
        print("\n✅ Conexión WiFi establecida")
    
    print(f"IP del nodo: {wlan.ifconfig()[0]}")

def leer_temperatura():
    try:
        sensor_dht.measure()
        temp = sensor_dht.temperature()
        hum = sensor_dht.humidity()
        return temp, hum
    except Exception as e:
        print("Error al leer sensor:", e)
        return None, None

def controlar_leds(temperatura):
    # Apagar todos los LEDs
    led_rojo.value(0)
    led_amarillo.value(0)
    led_verde.value(0)
    
    if temperatura is not None:
        if temperatura > 30:
            led_rojo.value(1)
            print(f"🔴 LED Rojo ENCENDIDO - Temp: {temperatura}°C")
        elif temperatura == 30:
            led_amarillo.value(1)
            print(f"🟡 LED Amarillo ENCENDIDO - Temp: {temperatura}°C")
        else:
            led_verde.value(1)
            print(f"🟢 LED Verde ENCENDIDO - Temp: {temperatura}°C")

def enviar_datos(temperatura, humedad, nodo_id, nombre_sensor):
    try:
        # Enviar a la IP fija del AP
        addr = socket.getaddrinfo("192.168.4.1", 8888)[0][-1]
        s = socket.socket()
        s.settimeout(10.0)
        s.connect(addr)
        
        datos = f"{nodo_id}:{nombre_sensor}:{temperatura},{humedad}"
        s.send(datos.encode('utf-8'))
        s.close()
        
        print(f"✅ Datos enviados: {nombre_sensor} ({nodo_id}) - Temp: {temperatura}°C, Hum: {humedad}%")
        return True
        
    except OSError as e:
        print(f"❌ Error de red al enviar datos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error general al enviar datos: {e}")
        return False

# === CONFIGURACIÓN DE CADA NODO ===
# Cambia estos valores en cada nodo esclavo:

# Nodo 1
NODO_ID = "sensor1"
NOMBRE_SENSOR = "SALA PRINCIPAL"

# Nodo 2: NODO_ID = "sensor2", NOMBRE_SENSOR = "COCINA"
# Nodo 3: NODO_ID = "sensor3", NOMBRE_SENSOR = "DORMITORIO 1"
# Nodo 4: NODO_ID = "sensor4", NOMBRE_SENSOR = "DORMITORIO 2"
# Nodo 5: NODO_ID = "sensor5", NOMBRE_SENSOR = "OFICINA"
# Nodo 6: NODO_ID = "sensor6", NOMBRE_SENSOR = "BAÑO"
# Nodo 7: NODO_ID = "sensor7", NOMBRE_SENSOR = "GARAJE"
# Nodo 8: NODO_ID = "sensor8", NOMBRE_SENSOR = "PATIO"

print("=== INICIANDO NODO ESCLAVO ===")
print(f"ID del nodo: {NODO_ID}")
print(f"Nombre del sensor: {NOMBRE_SENSOR}")

conectar_wifi()

# Esperar un poco antes de comenzar a enviar datos
print("⏳ Esperando 5 segundos antes de comenzar...")
time.sleep(5)

while True:
    temp, hum = leer_temperatura()
    if temp is not None and hum is not None:
        print(f"🔍 {NOMBRE_SENSOR} - Temperatura: {temp}°C | Humedad: {hum}%")
        controlar_leds(temp)
        
        if not enviar_datos(temp, hum, NODO_ID, NOMBRE_SENSOR):
            print(f"⚠ No se pudieron enviar datos, reintentando en 5 segundos...")
        
    else:
        print(f"⚠ Error en lectura del sensor del {NOMBRE_SENSOR}")
    
    time.sleep(5)
