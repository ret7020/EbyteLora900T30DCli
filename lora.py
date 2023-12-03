import serial
import time
import RPi.GPIO as GPIO

human_config_regs = {
    "02h": [ 
        {"000": 1200, "001": 2400, "010": 4800, "011": 9600, "100": 19200, "101": 38400, "110": 57600, "111": 115200}, # UART
        {"00": "8N1", "01": "8O1", "10": "8E1", "11": "8N1"}, # Parity bit
        {"010": "2.4k"} # Air data speed
    ]
}

# Init GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

# Init serial
ser = serial.Serial("/dev/serial0", 9600)
ser.flushInput()

# Push lora to setup mode (M1 == M0 == 1)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

GPIO.output(20, GPIO.HIGH)
GPIO.output(21, GPIO.HIGH)

#ser.write(b'\xC0\x05\x01\x04')
#print(ser.read(4))

if 0:
    print("--- Module config ---")
    ser.write(b"\xC1\x00\x04")
    config_regs = ser.read(7)
    print(config_regs)
    hex_regs = list(map(lambda x: hex(x)[2:], memoryview(config_regs)))
    reg_02h_parsed = bin(int(hex_regs[5]))[2:]
    reg_02h_parsed = "0" * (7 - (len(reg_02h_parsed))) + reg_02h_parsed
    print(reg_02h_parsed)
    print(f"Address    : {hex_regs[3]}.{hex_regs[4]}")
    print(f"UART speed : {human_config_regs['02h'][0][reg_02h_parsed[0:3]]}")
    print(f"Parity bit : {human_config_regs['02h'][1][reg_02h_parsed[3:5]]}")
    #print(f"Air speed  : {human_config_regs['02h'][2][reg_02h_parsed[5:8]]}")
    #ser.write(b"\xC1\x05\x01")
    #a = ser.read(3)
    #print(a)

ser.flushInput()
ser.flushOutput()
#print("Setting channel to 18 (0x12) - 868.125 MHz")
#ser.write(b"\xC0\x04\x01\x12")
#print(ser.read(4))
#ser.write(b"\xC1\x04\x01")
#print(ser.read(3))

# Push to transmit mode
GPIO.output(20, GPIO.LOW)
GPIO.output(21, GPIO.LOW)
#exit()
print("Starting transmission")
try:
    while 1:
        ser.write(b"\xFF\xFF\x12\xAA")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
    ser.close()
    print("Bye")
    exit(0)
#ser.write("some\n".encode())
