# tn-picopi-lcd
** control a pico-pi with an lcd to display truenas system - pool - app info **

<a href="https://postimg.cc/TK4YyMPK" target="_blank"><img src="https://i.postimg.cc/TK4YyMPK/Screenshot-2025-03-30-200450.png" alt="Screenshot-1"/></a> <a href="https://postimg.cc/t1nRWS12" target="_blank"><img src="https://i.postimg.cc/t1nRWS12/Screenshot-2025-03-30-200523.png" alt="Screenshot-2"/></a> <a href="https://postimg.cc/TL8d9VgG" target="_blank"><img src="https://i.postimg.cc/TL8d9VgG/Screenshot-2025-03-30-200542.png" alt="Screenshot-3"/></a><br/><br/>


---

### What you need:
Consider that this is not mandatory, you can use whatever you want. But for me this was really cheap (5€ total expense) and pain free setup:
<ul>
    <li> a Pico PI controller board </li>
    <li> a 16x2 LCD with L2c interface </li>
    <li> 4 wire </li>
    <li> 1 USB cable </li>
</ul>

### Before you start:
I used this guide >> https://www.circuitschools.com/interfacing-16x2-lcd-module-with-raspberry-pi-pico-with-and-without-i2c/
to interface the Pico to the LCD, but follow whatever tutorial you pref

### What those script do:
>> The  `main.py` put the Pico listening to the serial port of the USB where he get attacched, automatically. You can grab the correct one using `sudo dmesg | grep tty`
>> The `TN_Pico_LCD.py` contains some istruction to retrieve and manipulate data to show, most obtained via Truenas API.

Every 8s a new info will be displayed.

### How to use those script:
Istructions are really simple:
<ul>
    <li> save the `main.py` into your Pico; adjust the initial variables on your needs </li>
    <li> save the `TN_Pico_LCD.py` in your system, <b>in a secured folder/dataset</b></li>
    <li> connect the Pico, he will put itself on listening to the USB port </li>
    <li> launch the script to test </li>
</ul>

you can set the script as startup script to let he start automatically on reboot.

### Example usage:
`cd /mnt/Pool/Tank/SecureDataset && python TN_Pico_LCD.py /dev/ttyACM0`

### What actually is displayed:
<ul>
    <li> CPU Temperature </li>
    <li> CPU Usage</li>
    <li> Total RAM</li>
    <li> Used RAM</li>
    <li> Pool Section: name, status, health, free space percentage</li>
    <li> IX App Section: name, state, if upgrade is available</li>      
</ul>



