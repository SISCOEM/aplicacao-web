from serial.tools import list_ports
import threading
import serial
import time
import simpleaudio as sa


command_hex = "AA 00 27 00 03 22 FF FF 4A DD"
# command_hex_2 = "AA 00 B6 00 02 03 E8 A3 DD"
command_hex_3 = "AA 00 F5 00 01 00 F6 DD"
command_hex_2 = "AA 00 B6 00 02 07 D0 8F DD"

"AA 00 39 00 09 00 00 00 00 03 00 00 00 08 4D DD" # lê
"AA 01 B6 00 01 00 B8 DD"

time_while = 60 * 60 * 100

def send_hex_command(ser, commands=[command_hex_2, command_hex_3, command_hex]):
    print('Writing Command')
    if ser.is_open:
        try:
            if isinstance(commands, str):
                ser.write(bytearray.fromhex(commands))
                print('Sent command:', commands)
            elif isinstance(commands, list):
                for cmd in commands:
                    time.sleep(0.5)
                    ser.write(bytearray.fromhex(cmd))
                    print('Sent command:', cmd)
        except Exception as e:
            print('Error sending command:', str(e))


def is_iterable(variable):
    try:
        iter(variable)
        return True
    except TypeError:
        return False
    

def verificar_portas(sensor):
    if sensor == "DIGITAL_READER":
        for porta in list_ports.comports():
            if "CH340" in porta.description.upper():
                try:
                    ser = serial.Serial(porta.device, baudrate=115200, timeout=2)
                    print(f"Tentando porta {porta.device}...")
                    
                    for _ in range(10000):
                        time.sleep(1)
                        try:
                            resposta = ser.readline().decode('UTF-8')
                            print(resposta)
                            if "FINGERPRINT::SUCCESS::Started" in resposta:
                                print(f"Mensagem 'started' recebida em {porta.device}")
                                ser.write("4".encode())
                                return porta.device
                        except UnicodeDecodeError:
                            print(f"Erro de decodificação em {porta.device}: impossível decodificar como UTF-8")
                    ser.write("4".encode())
                    ser.close()

                except serial.SerialException:
                    print(f"Erro ao abrir a porta {porta.device}")
            else:
                print(f"Porta {porta.device} descartada, description: {porta.description.upper()}")
                
    elif sensor == "RFID_MODULE":
        for porta in list_ports.comports():
            if "CH340" in porta.description.upper():
                try:
                    ser = serial.Serial(porta.device, baudrate=115200, timeout=2)
                    print(f"device {ser}...")
                    print(f"Tentando porta {porta.device}...")
                    
                    for _ in range(10000):
                        time.sleep(1)
                        send_hex_command(ser, "AA 00 08 00 08 DD")
                        try:
                            resposta = read_line(ser, read_tag=False, timer=2)
                            if is_iterable(resposta) and "AA" in resposta and "DD" in resposta:
                                print(f"Modulo RFID recebido {porta.device}")
                                return porta.device
                            else:
                                send_hex_command(ser, "AA 00 08 00 08 DD")
                                resposta = read_line(ser, timer=3)
                                print(resposta)
                                
                                if is_iterable(resposta) and "aa" in resposta and "dd" in resposta:
                                    print(f"Modulo RFID recebido {porta.device}")
                                    return porta.device
                                
                        except UnicodeDecodeError:
                            print(f"Erro de decodificação em {porta.device}: impossível decodificar como UTF-8")
                    ser.write("4".encode())
                    ser.close()

                except serial.SerialException:
                    print(f"Erro ao abrir a porta {porta.device}")
            else:
                print(f"Porta {porta.device} descartada, description: {porta.description.upper()}")
        

def read_line(ser, start_time=time.time(), timer=time_while, read_tag=True):
    is_reading = False
    read_data = []
    print("Reading")

    while time.time() - start_time < timer:
        rc = ser.read(1)
        
        if rc == b'\xAA':
            is_reading = True
            current_read_length = 0
            read_data = []

        if is_reading:
            read_data.append(rc.hex().upper())

            if current_read_length == 1:
                if read_tag and rc != b'\x02':
                    is_reading = False
                    read_data = []

            if rc == b'\xDD':
                return read_data

            current_read_length += 1


def get_uids():
    from SICOMB.settings import AUX, STATICFILES_DIRS
    
    while not AUX['serial_port_rfid'].isOpen():
        time.sleep(1)
        AUX['serial_port_rfid'].open()
        
    ser = AUX['serial_port_rfid']
    
    print("\nConexão com sensor RFID configurada com sucesso!\n")
    time.sleep(1)
    send_hex_command(ser)
    
    start_time = time.time()
    
    while time.time() - start_time < time_while:
        try:
            line = read_line(ser, start_time)
            
            line = "".join(line[6:len(line) - 2])

            print(AUX["uids"])
            if line not in AUX["uids"] and line.strip() != "" :
                AUX["uids"].append(line)
                som = sa.WaveObject.from_wave_file(STATICFILES_DIRS[0] + "/sounds/passSound.wav")
                play_obj = som.play()
                play_obj.wait_done()
                
        except UnicodeDecodeError:
            print(f"Erro de decodificação no sensor RFID, impossível decodificar como UTF-8")
        except Exception as e:
            print("\nConexão com sensor RFID perdida!\n")
            print(e)
            time.sleep(1)
            
            if not ser.isOpen():
                print("Conexão serial perdida. Tentando reconectar...")
                ser.open()
            
            if AUX['serial_port_rfid'].is_open:
                AUX['serial_port_rfid'].close()
            
            while not ser.is_open:
                try:
                    if not ser.isOpen():
                        print("Conexão serial perdida. Tentando reconectar...")
                        ser.open()
                    else:
                        break
                except Exception as e:
                    time.sleep(1)
                    print(e)
                    
            send_hex_command(ser)
            print("\nConexão reestabelecida!\n")
            print(f"ser.is_open {ser.is_open}\n ")
    
    ser.close()
    print("\n\nThread get_uids stopped\n\n")
        
    

def get_fingerprint():
    from SICOMB.settings import AUX
    
    print("\nConexão com sensor leitor de impressão digital configurada com sucesso!\n")
    
    ser = AUX['serial_port_fingerprint']
    
    while True:
        try:
            line = ser.readline().decode('utf-8')
            print(line)
            if not line:
                continue
            line = line.split("::")
        
            if len(line) > 1:
                AUX["message_fingerprint_sensor"] = line
        except UnicodeDecodeError:
            print(f"Erro de decodificação no sensor de impressão digital, impossível decodificar como UTF-8")
        except Exception as e:
            print("\nConexão com sensor leitor de impressão digital perdida!\n")
            print(e)
            AUX["message_fingerprint_sensor"] = ['FINGERPRINT', 'ERROR', 'Conexão com sensor leitor de impressão digital perdida!']
            
            if AUX['serial_port_fingerprint'].is_open:
                AUX['serial_port_fingerprint'].close()
            
            while not ser.is_open:
                time.sleep(1)
                try:
                    if ser.is_open: ser.close()
                    ser = serial.Serial(AUX["PORT_FINGERPRINT"], 115200)
                    AUX['serial_port_fingerprint'] = ser
                except Exception as e:
                    print(e)
            print("\nConexão reestabelecida!\n")

from SICOMB.settings import AUX

def get_connection():
    AUX['PORT_RFID'] = verificar_portas("RFID_MODULE")
    
    ser_rfid = None
    while True:
        try:
            if ser_rfid is not None:
                ser_rfid.close()
            ser_rfid = serial.Serial(AUX['PORT_RFID'], 115200, timeout=2)
            if ser_rfid.is_open:
                break
        except Exception as e:
            print(e)
            time.sleep(0.5)
            
    AUX['serial_port_rfid'] = ser_rfid
        

if AUX["SENSOR_RFID"]:
    get_connection()
    
    threading.Thread(target=get_uids).start()
    
    def restart_event():
        send_hex_command(AUX['serial_port_rfid'])
            
    AUX['restart_rfid_thread'] = restart_event
    

if AUX["SENSOR_FINGERPRINT"]:
    AUX['PORT_FINGERPRINT'] = verificar_portas("DIGITAL_READER")
    
    ser_fingerprint = None
    while ser_fingerprint is None:
        try:
            if ser_fingerprint is not None: ser_fingerprint.close()
            ser_fingerprint = serial.Serial(AUX['PORT_FINGERPRINT'], 115200)
            time.sleep(2)
            ser_fingerprint.write("4".encode())
        except Exception as e:
            time.sleep(0.5)
            print(e)
        
    AUX['serial_port_fingerprint'] = ser_fingerprint
    
    THREAD_FINGERPRINT = threading.Thread(target=get_fingerprint)
    THREAD_FINGERPRINT.start()
