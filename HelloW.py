from machine import Pin, I2C
import ssd1306

# --- Configuración (ajusta si es necesario) ---
SDA_PIN = 21  # Pin GPIO para SDA (data)
SCL_PIN = 22  # Pin GPIO para SCL (clock)
OLED_WIDTH = 128
OLED_HEIGHT = 64 # O 32, según tu pantalla

# --- Inicialización I2C ---
i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)

# --- Búsqueda y Inicialización del Display ---
devices = i2c.scan()
if devices:
    print(f"OLED encontrado en la dirección: {hex(devices[0])}")
    display = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=devices[0])
    
    # --- Mostrar "Hello, World!" ---
    display.fill(0)          # Limpia la pantalla (rellena con negro)
    display.text("Hello,", 0, 0, 1) # Escribe "Hello," en la esquina superior izquierda (0,0) en blanco (1)
    display.text("World!", 0, 10, 1) # Escribe "World!" debajo de "Hello," (0,10) en blanco (1)
    display.show()           # Actualiza el display para mostrar los cambios
else:
    print("No se encontraron dispositivos I2C. Revisa el cableado.")