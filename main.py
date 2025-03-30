import machine
import utime
import sys
import select
from pico_i2c_lcd import I2cLcd

PIN_SDA = 8
PIN_SCL = 9
FREQ = 400000
ADDR = 0x27
ROW = 2
COL = 16

i2c = machine.I2C(0, sda=machine.Pin(PIN_SDA), scl=machine.Pin(PIN_SCL), freq=FREQ)
lcd = I2cLcd(i2c, ADDR, ROW, COL)  

counter = 0
lcd.clear()
message = "Waiting data"
lcd.putstr(message)

while True:
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        message = sys.stdin.readline().strip()
        try:
            label, value = message.split(":", 1)
            lcd.clear()
            
            lcd.move_to(0, 0)
            lcd.putstr(label)
            
            lcd.move_to(0, 1)
            lcd.putstr(value)
        except ValueError:
            pass
        counter = 0
        utime.sleep(4.0)     
    else:      
        lcd.clear()
        lcd.move_to(0, 1)
        if (counter == 0):
            lcd.putstr("")
            counter = counter +1
        elif (counter == 1):
            lcd.putstr(".")
            counter = counter +1
        elif (counter == 2):
            lcd.putstr("..")
            counter = counter +1
        elif (counter >= 3):
            lcd.putstr("...")
            counter = 0    
        utime.sleep(2.5)