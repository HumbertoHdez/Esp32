# Importa la clase Pin para controlar los pines GPIO del ESP32.
# Importa la clase I2C para establecer la comunicación I2C (Inter-Integrated Circuit).
from machine import Pin, I2C
# Importa el módulo time para usar funciones relacionadas con el tiempo, como delays (retardos).
import time
# Importa la librería ssd1306, que contiene el driver para controlar las pantallas OLED SSD1306.
# NOTA: Debes asegurarte de que el archivo 'ssd1306.py' esté subido a tu ESP32.
import ssd1306

# --- Configuración del Hardware y Display ---
# Define el número del pin GPIO del ESP32 que se usará como SDA (Serial Data Line) para I2C.
SDA_PIN = 21
# Define el número del pin GPIO del ESP32 que se usará como SCL (Serial Clock Line) para I2C.
SCL_PIN = 22
# Define el ancho de la pantalla OLED en píxeles. Las pantallas comunes son de 128 píxeles de ancho.
OLED_WIDTH = 128
# Define la altura de la pantalla OLED en píxeles. Puede ser 64 o 32, dependiendo de tu modelo de display.
OLED_HEIGHT = 64

# --- Inicialización del Bus I2C ---
# Crea una instancia del objeto I2C.
# I2C(0): Selecciona el bus I2C número 0 del ESP32.
# sda=Pin(SDA_PIN): Asigna el pin GPIO definido como SDA para la comunicación I2C.
# scl=Pin(SCL_PIN): Asigna el pin GPIO definido como SCL para la comunicación I2C.
# freq=400000: Establece la frecuencia del reloj I2C a 400 kHz (kilohertz), una velocidad común para estos displays.
i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)

# --- Inicialización del Display OLED ---
# Escanea el bus I2C en busca de dispositivos conectados y devuelve una lista de sus direcciones.
devices = i2c.scan()
# Comprueba si se encontraron dispositivos en el bus I2C.
if devices:
    # Si se encuentra al menos un dispositivo, imprime su dirección I2C en formato hexadecimal.
    print(f"Dispositivo(s) I2C encontrado(s): {hex(devices[0])}")
    # Crea una instancia del driver SSD1306 para el display OLED.
    # OLED_WIDTH, OLED_HEIGHT: Pasa las dimensiones del display.
    # i2c: Pasa el objeto I2C ya inicializado.
    # addr=devices[0]: Usa la dirección del primer dispositivo I2C encontrado (generalmente 0x3C o 0x3D para OLEDs).
    display = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=devices[0])
else:
    # Si no se encuentran dispositivos I2C, imprime un mensaje de error.
    print("No se encontraron dispositivos I2C. Revisa el cableado.")
    # La función 'exit()' no está disponible en MicroPython.
    # En un entorno real de MicroPython, esta línea causaría un 'NameError'.
    # Para manejar esto, deberías evitar usar el display o entrar en un bucle infinito.
    exit() # Esta línea causará un error en MicroPython; se debería manejar de otra forma.

# --- Funciones para Controlar el Display ---

def clear_display():
    """
    Limpia completamente el contenido del display OLED.
    """
    # Rellena todo el búfer de la pantalla con el color 0 (negro).
    display.fill(0)
    # Envía el contenido del búfer (la pantalla limpia) al display físico para que se muestre.
    display.show()

def write_text(text, x, y, color=1):
    """
    Escribe texto en el display OLED.

    Args:
        text (str): La cadena de texto a escribir.
        x (int): La coordenada X (columna) donde comenzará el texto (0 es el borde izquierdo).
        y (int): La coordenada Y (fila) donde comenzará el texto (0 es el borde superior).
        color (int): El color del texto. 1 para blanco (píxel encendido), 0 para negro (píxel apagado).
                     El valor por defecto es blanco.
    """
    # Dibuja el texto especificado en las coordenadas (x, y) con el color dado.
    display.text(text, x, y, color)
    # Actualiza el display para mostrar el texto dibujado.
    display.show()

def draw_pixel(x, y, color=1):
    """
    Dibuja un solo píxel en el display OLED.

    Args:
        x (int): La coordenada X del píxel.
        y (int): La coordenada Y del píxel.
        color (int): El color del píxel. 1 para blanco, 0 para negro. Por defecto es blanco.
    """
    # Dibuja un píxel en las coordenadas (x, y) con el color especificado.
    display.pixel(x, y, color)
    # Actualiza el display para mostrar el píxel.
    display.show()

def draw_line(x1, y1, x2, y2, color=1):
    """
    Dibuja una línea en el display OLED.

    Args:
        x1 (int): Coordenada X del punto de inicio de la línea.
        y1 (int): Coordenada Y del punto de inicio de la línea.
        x2 (int): Coordenada X del punto final de la línea.
        y2 (int): Coordenada Y del punto final de la línea.
        color (int): El color de la línea. 1 para blanco, 0 para negro. Por defecto es blanco.
    """
    # Dibuja una línea desde (x1, y1) hasta (x2, y2) con el color especificado.
    display.line(x1, y1, x2, y2, color)
    # Actualiza el display para mostrar la línea.
    display.show()

def draw_rectangle(x, y, width, height, color=1, fill=False):
    """
    Dibuja un rectángulo en el display OLED.

    Args:
        x (int): Coordenada X de la esquina superior izquierda del rectángulo.
        y (int): Coordenada Y de la esquina superior izquierda del rectángulo.
        width (int): El ancho del rectángulo en píxeles.
        height (int): La altura del rectángulo en píxeles.
        color (int): El color del rectángulo. 1 para blanco, 0 para negro. Por defecto es blanco.
        fill (bool): Si es True, el rectángulo se rellena con el color. Si es False, solo se dibuja el contorno.
    """
    # Comprueba si el rectángulo debe ser rellenado o solo el contorno.
    if fill:
        # Dibuja un rectángulo relleno con el color especificado.
        display.fill_rect(x, y, width, height, color)
    else:
        # Dibuja solo el contorno de un rectángulo con el color especificado.
        display.rect(x, y, width, height, color)
    # Actualiza el display para mostrar el rectángulo.
    display.show()

# --- Ejemplo de Uso de las Funciones del Display ---
# Este bloque de código se ejecuta solo cuando el script se corre directamente (no cuando se importa como módulo).
if __name__ == "__main__":
    # Llama a la función para limpiar el display, dejándolo en negro.
    clear_display()
    # Pausa la ejecución por 1 segundo.
    time.sleep(1)

    # Imprime un mensaje en la consola serial del ESP32.
    print("Escribiendo texto...")
    # Escribe "Hola ESP32!" en la esquina superior izquierda del display.
    write_text("Hola ESP32!", 0, 0)
    # Escribe "MicroPython" en la siguiente línea (10 píxeles más abajo).
    write_text("MicroPython", 0, 10)
    # Escribe "OLED I2C" en la siguiente línea (20 píxeles más abajo).
    write_text("OLED I2C", 0, 20)
    # Pausa la ejecución por 2 segundos para que el usuario pueda leer el texto.
    time.sleep(2)

    # Imprime un mensaje en la consola serial.
    print("Dibujando formas...")
    # Limpia el display para preparar el dibujo de nuevas formas.
    clear_display()
    # Dibuja una línea diagonal desde la esquina superior izquierda hasta la esquina inferior derecha.
    draw_line(0, 0, OLED_WIDTH - 1, OLED_HEIGHT - 1)
    # Dibuja un rectángulo sin rellenar en las coordenadas (10, 30) con un tamaño de 50x20 píxeles.
    draw_rectangle(10, 30, 50, 20, fill=False)
    # Dibuja un rectángulo relleno en las coordenadas (70, 40) con un tamaño de 30x15 píxeles, en blanco.
    draw_rectangle(70, 40, 30, 15, color=1, fill=True)
    # Pausa la ejecución por 3 segundos.
    time.sleep(3)

    # Imprime un mensaje en la consola serial.
    print("Píxel por píxel...")
    # Limpia el display.
    clear_display()
    # Bucle que itera a través de cada columna del display.
    for i in range(OLED_WIDTH):
        # Dibuja un píxel en la columna 'i' y en una fila que cambia con 'i' (creando un patrón).
        draw_pixel(i, i % OLED_HEIGHT)
        # Pequeña pausa para que el dibujo de cada píxel sea visible.
        time.sleep(0.01)
    # Pausa la ejecución por 2 segundos.
    time.sleep(2)

    # Limpia el display por última vez.
    clear_display()
    # Escribe "Demo Completa!" en la esquina superior izquierda.
    write_text("Demo Completa!", 0, 0)
    # Imprime un mensaje final en la consola serial.
    print("Demo completa.")