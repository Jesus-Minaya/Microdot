def connect_to(ssid, passwd):
    """
        Conecta el microcontrolador a la red WIFI
        
        ssid (str): Nombre de la red WIFI
        passwd (str): Clave de la red WIFI
        
        returns (str): Retorna la direccion de IP asignada
    """
    import network
    # Creo una instancia para interfaz tipo station
    sta_if = network.WLAN(network.STA_IF)
    # Verifico que no este conectado ya a la red
    if not sta_if.isconnected():
        # Activo la interfaz
        sta_if.active(True)
        # Intento conectar a la red
        sta_if.connect('Red Alumnos', '')
        # Espero a que se conecte
        while not sta_if.isconnected():
            pass
        # Retorno direccion de IP asignada
    return sta_if.ifconfig()[0]
        
# Importo lo necesario para la aplicacion de Microdot
from microdot import Microdot, send_file

# Creo una instancia de Microdot
app = Microdot()

@app.route("/")
@app.route("/")
def index(request):
    """
    Funcion asociada a la ruta principal de la aplicacion
    
    request (Request): Objeto que representa la petición del cliente
    
    returns (File): Retorna un archivo HTML
    """
    return send_file("templates/index.html")

@app.route("/assets/<dir>/<file>")
def assets(request, dir, file):
    """
    Funcion asociada a una ruta que solicita archivos CSS o JS
    
    request (Request): Objeto que representa la peticion del cliente
    dir (str): Nombre del directorio donde esta el archivo
    file (str): Nombre del archivo solicitado
    
    returns (File): Retorna un archivo CSS o JS
    """
    return send_file("/assets/" + dir + "/" + file)

@app.route("/data/update")
def data_update(request):
    """
    Funcion asociada a una ruta que solicida datos del microcontrolador
    
    request (Request): Objeto que representa la peticion del cliente
    
    returns (dict): Retorna un diccionario con los datos leidos
    """
    # Importo ADC para lectura analogica
    from machine import Pin, SoftI2C

    # Configurar los pines SDA y SCL
    sda_pin = Pin(4)  # Reemplazar con el número correcto del pin GPIO para SDA
    scl_pin = Pin(5)  # Reemplazar con el número correcto del pin GPIO para SCL

    # Inicializar el objeto SoftI2C
    i2c = SoftI2C(sda=sda_pin, scl=scl_pin, freq=100000)


    # Dirección I2C del MPU-92/65 (sustituir con la dirección correcta)
    mpu_address = 0x69

    # Configurar el sensor de temperatura para una única medición
    i2c.writeto_mem(mpu_address, 0x6B, b'\x01')  # Habilitar el sensor

    # Configurar el registro de control para la lectura de temperatura
    i2c.writeto_mem(mpu_address, 0x6A, b'\x80')  # Configurar para habilitar la lectura de temperatura

    # Leer la temperatura del MPU-92/65
    while True:
        temp_data = i2c.readfrom_mem(mpu_address, 0x41, 2)
        temperature = ((temp_data[0] << 8) | temp_data[1]) / 333.87 + 21.0
        print("Temperatura:", temperature, "grados Celsius")
        utime.sleep_ms(1000)  # Esperar 1 segundo antes de la próxima lectura
    # Retorno el diccionario
    return { "cpu_temp" : temperatura_cpu }
    


# Programa principal, verifico que el archivo sea el main.py
if __name__ == "__main__":
    
    try:
        # Me conecto a internet
        ip = connect_to('Red Alumnos', '')
        # Muestro la direccion de IP
        print("Microdot corriendo en IP/Puerto: " + ip + ":5000")
        # Inicio la aplicacion
        app.run()
    
    except KeyboardInterrupt:
        # Termina el programa con Ctrl + C
        print("Aplicacion terminada")