import network
import socket
import time
from machine import Pin
ap = network.WLAN(network.AP_IF)
ap.config(essid="RedESP32", password="miclave123", authmode=network.AUTH_WPA_WPA2_PSK)
ap.active(True)
ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
print("📶 AP listo. IP: 192.168.4.1")
# Sensor 1
s1_verde = Pin(12, Pin.OUT)
s1_amarillo = Pin(13, Pin.OUT)
s1_rojo = Pin(14, Pin.OUT)
s2_verde = Pin(25, Pin.OUT)
s2_amarillo = Pin(26, Pin.OUT)
s2_rojo = Pin(27, Pin.OUT)
estado = {"sensor1": None, "sensor2": None}
def actualizar_leds():
    # Sensor 1
    if estado["sensor1"] is not None:
        temp = estado["sensor1"]
        s1_verde.off()
        s1_amarillo.off()
        s1_rojo.off()
        if temp < 30:
            s1_verde.on()
        elif temp == 30:
            s1_amarillo.on()
        else:
            s1_rojo.on()
    if estado["sensor2"] is not None:
        temp = estado["sensor2"]
        s2_verde.off()
        s2_amarillo.off()
        s2_rojo.off()
        if temp < 30:
            s2_verde.on()
        elif temp == 30:
            s2_amarillo.on()
        else:
            s2_rojo.on()
s1_verde.off(); s1_amarillo.off(); s1_rojo.off()
s2_verde.off(); s2_amarillo.off(); s2_rojo.off()
print("💡 LEDs apagados al inicio.")
servidor = socket.socket()
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(('0.0.0.0', 8888))
servidor.listen(2)
print("📡 Esperando datos de sensores...\n")
while True:
    try:
        cliente, addr = servidor.accept()
        data = cliente.recv(64)
        if len(data) > 0:
            msg = data.decode().strip()
            if ":" in msg:
                sensor_id, valores = msg.split(":", 1)
                if sensor_id in ("sensor1", "sensor2") and "," in valores:
                    try:
                        temp_str, _ = valores.split(",", 1)
                        temp = int(float(temp_str))
                        estado[sensor_id] = temp
                        print(f"✅ {sensor_id} → {temp}°C")
                        actualizar_leds()
                    except:
                        print(f"⚠  Dato inválido de {sensor_id}")
        cliente.close()
    except Exception as e:
        print("❌ Error:", e)
        time.sleep(1)
