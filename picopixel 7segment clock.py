#import machine
from machine import Pin, PWM, RTC, Timer
import time

rtc = RTC()
c1 = machine.Pin(5, machine.Pin.OUT)
c2 = machine.Pin(6, machine.Pin.OUT)
c3 = machine.Pin(7, machine.Pin.OUT)
c4 = machine.Pin(8, machine.Pin.OUT)

segment_pins = [
     machine.Pin(11, machine.Pin.OUT),
     machine.Pin(9, machine.Pin.OUT),
     machine.Pin(13, machine.Pin.OUT),
     machine.Pin(15, machine.Pin.OUT),
     machine.Pin(16, machine.Pin.OUT),
     machine.Pin(10, machine.Pin.OUT),
     machine.Pin(12, machine.Pin.OUT),
     machine.Pin(14, machine.Pin.OUT),
]

button1 = machine.Pin(0, machine.Pin.IN)
button2 = machine.Pin(1, machine.Pin.IN)
button3 = machine.Pin(3, machine.Pin.IN)
button4 = machine.Pin(4, machine.Pin.IN)
button5 = machine.Pin(26, machine.Pin.IN)
button6 = machine.Pin(27, machine.Pin.IN)
relay = PWM(machine.Pin(2, machine.Pin.IN))


led_pin = Pin("LED", Pin.OUT)		#hardware časovač pro blikání s LED "dvoutečkou" - po inicializaci nezatěžuje jádro.
tim = Timer()  # Create an instance of Timer

def toggle_led(t):
    led_pin.value(not led_pin.value())
    
# Initialize the timer
tim.init(mode=Timer.PERIODIC, period=500, callback=toggle_led)

chars = {
    #      a  b  c  d  e  f  g  dp	#pouze pro zobrazení jednotlivých segmentů displeje - testování atd...
    "a":  [1, 0, 0, 0, 0, 0, 0, 0],
    "b":  [0, 1, 0, 0, 0, 0, 0, 0],
    "c":  [0, 0, 1, 0, 0, 0, 0, 0],
    "d":  [0, 0, 0, 1, 0, 0, 0, 0],
    "e":  [0, 0, 0, 0, 1, 0, 0, 0],
    "f":  [0, 0, 0, 0, 0, 1, 0, 0],
    "g":  [0, 0, 0, 0, 0, 0, 1, 0],
    "dp": [0, 0, 0, 0, 0, 0, 0, 1],
    }

letters = {
    #     a  b  c  d  e  f  g  dp 	bacha, funkce je case-sensitive -> pozor na mal8 a velká písmena
    " ": [0, 0, 0, 0, 0, 0, 0, 0],
    "0": [1, 1, 1, 1, 1, 1, 0, 0], # zde můžeš pridávat libovolně své znaky pro zobrazování
    "1": [0, 1, 1, 0, 0, 0, 0, 0],
    "2": [1, 1, 0, 1, 1, 0, 1, 0],
    "3": [1, 1, 1, 1, 0, 0, 1, 0],
    "4": [0, 1, 1, 0, 0, 1, 1, 0],
    "5": [1, 0, 1, 1, 0, 1, 1, 0],
    "6": [1, 0, 1, 1, 1, 1, 1, 0],
    "7": [1, 1, 1, 0, 0, 0, 0, 0],
    "8": [1, 1, 1, 1, 1, 1, 1, 0],
    "9": [1, 1, 1, 1, 0, 1, 1, 0],
    "a": [1, 1, 1, 0, 1, 1, 1, 0],
    "b": [0, 0, 1, 1, 1, 1, 1, 0],
    "c": [1, 0, 0, 1, 1, 1, 0, 0],
    "d": [0, 1, 1, 1, 1, 0, 1, 0],
    "e": [1, 0, 0, 1, 1, 1, 1, 0],
    "f": [1, 0, 0, 0, 1, 1, 1, 0],
    "g": [1, 0, 1, 1, 1, 1, 0, 0],	#ne všechny znaky jsou spávně nastavené, je potřeba doplnit
    "h": [1, 0, 0, 0, 1, 1, 1, 0],
    "i": [1, 0, 0, 0, 1, 1, 1, 0],
    "j": [0, 1, 1, 1, 1, 0, 0, 0],
    "k": [1, 0, 0, 0, 1, 1, 1, 0],
    "l": [0, 0, 0, 1, 1, 1, 0, 0],
    "m": [1, 0, 0, 0, 1, 1, 1, 0],
    "n": [0, 0, 1, 0, 1, 1, 1, 0],
    "o": [1, 1, 1, 1, 1, 1, 0, 0],
    "p": [1, 0, 0, 0, 1, 1, 1, 0],
    "q": [1, 0, 0, 0, 1, 1, 1, 0],
    "r": [1, 0, 0, 0, 1, 1, 0, 0],
    "s": [1, 0, 0, 0, 1, 1, 1, 0],
    "t": [1, 0, 0, 0, 1, 1, 1, 0],
    "u": [1, 0, 0, 0, 1, 1, 1, 0],
    "v": [0, 1, 1, 1, 1, 1, 0, 0],
    "w": [1, 0, 0, 0, 1, 1, 1, 0],
    "x": [1, 0, 0, 0, 1, 1, 1, 0],
    "y": [1, 0, 0, 0, 1, 1, 1, 0],
    "z": [1, 1, 0, 1, 1, 0, 1, 0],
    }

def seg_print(segment): #zobrazí pouze jeden segment (dobré pro testování atd, nikoli pro zobrazování dat) - možné vstupní parametry a,b,c,d,e,f,g,dp. použití např. seg_print(a). je potřeba zapnout digit pomocí zapsání "1" do nějakého z výstupu "c" , např. "c1.value(1)" pro spuštění 1. digitu displeje
    vals = chars[segment]
    for segment_number in range(0, 8):
        segment_pins[segment_number].value(vals[segment_number])
        
def seg_print_letter(x):#zobrazí znak ze setu "letters". jako argument bere čísla (int) i znaky (char, popř jeden znak string), je potřeba zapnout digit pomocí zapsání "1" do nějakého z výstupu "c" , např. "c1.value(1)" pro spuštění 1. digitu displeje
    x = str(x)  # Převod na string
    if x in letters:
        vals = letters[x]
        for segment_number in range(8):
            segment_pins[segment_number].value(vals[segment_number])
    else:
        print(f"Neznámý znak: {x}")#pokud znak naní v setu "letters", vypíše do konzole.
        time.sleep_us(100000)
        

def show_number(number): #zobrazí na displeji číslo (int). zobrazí jen 4 poslední číslice, ostatní vyplní nulami. použití např. show_number(12)
    if isinstance(number, int):
        seg_print_letter((number%10000)//1000)  
        c1.value(1)
        time.sleep_us(100)
        c1.value(0)

        seg_print_letter((number%1000)//100)
        c2.value(1)
        time.sleep_us(100)
        c2.value(0)

        seg_print_letter((number%100)//10)
        c3.value(1)
        time.sleep_us(100)
        c3.value(0)

        seg_print_letter(number%10)
        c4.value(1)
        time.sleep_us(100)
        c4.value(0)
    else:
        print("špatný datový typ")
        time.sleep_us(100000)
    
def show_number1(number): #zobrazí na displeji číslo (int). zobrazí jen 4 poslední číslice, ostatní nezobrazí. použití např. show_number(12)
    if isinstance(number, int): #kontrola, zda je předaná hodnota opravdu typu int (celé číslo), jinak nezobrazí nic
        if (number//1000):
            seg_print_letter((number%10000)//1000)  
            c1.value(1)
            time.sleep_us(100)
            c1.value(0)

        if (number//100):
            seg_print_letter((number%1000)//100)
            c2.value(1)
            time.sleep_us(100)
            c2.value(0)

        if (number//10):
            seg_print_letter((number%100)//10)
            c3.value(1)
            time.sleep_us(100)
            c3.value(0)

        if (number):
            seg_print_letter(number%10)
            c4.value(1)
            time.sleep_us(100)
            c4.value(0)
    else:
        print("špatný datový typ")
        time.sleep_us(100000)

def show_string(string): #zobrazí na displeji string. délka stringu může být libovolná, ale zobrazí jen 4 poslední znaky. použití např.  show_string("ade")
    if isinstance(string, str): #kontrola, zda je předaná hodnota opravdu typu string, jinak nezobrazí nic
        if (len(string)>3):
            seg_print_letter(string[-4]) 
            c1.value(1)
            time.sleep_us(100)
            c1.value(0)
            
        if (len(string)>2):
            seg_print_letter(string[-3])
            c2.value(1)
            time.sleep_us(100)
            c2.value(0)
            
        if (len(string)>1):
            seg_print_letter(string[-2])
            c3.value(1)
            time.sleep_us(100)
            c3.value(0)
            
        if (len(string)):
            seg_print_letter(string[-1])
            c4.value(1)
            time.sleep_us(100)
            c4.value(0)
    else:
        print("špatný datový typ")
        time.sleep_us(100000)
    
    
def set_time_epoch(sec):	#nastaví čas vnitřních RTC hodin na epoch time (čas v sekundách od roku 1970)
    # Convert epoch seconds to a tuple: (year, month, mday, hour, minute, second, weekday, yearday)
    dt = time.localtime(sec)
    # dt = (year, month, mday, hour, minute, second, weekday, yearday)

    # Set the RTC with the datetime tuple
    rtc = machine.RTC()
    rtc.datetime((dt[0], dt[1], dt[2], 0, dt[3], dt[4], dt[5], 0))

rtc.datetime((2020, 1, 21, 2, 10, 32, 36, 0))
while True: #nekonečná smyčka, zde piš program
    
    #show_number1(1)
    #show_string("zdar")	#aby bylo vidět zobrazené data, je potřeba volat funkci hodně často - na displeji je vždy zobrazený maximálně jeden digit. iluze toho, že jich svítí víc je zpusobena tím, že oči jsou "pomalé"
    show_number(time.localtime()[3]*100 +time.localtime()[4])
    
    i = 0
    while button1.value():
        i += 5	#pro postupne zrychlovani upravy casu
        if i > 20000:
            i = 20000
        time.sleep_us(500)
        set_time_epoch(time.time()+i//200)	# // je celociselne deleni
        show_number(time.localtime()[3]*100 +time.localtime()[4])

    while (button2.value() or button3.value()):
        i += 1
        if i >> 5:
            i=0
            if button2.value():
                set_time_epoch(time.time()+1)
            if button3.value():
                set_time_epoch(time.time()-2)    
        x = 0        
        while (button2.value() and button3.value()):	#prekvapeni :)
            x += 1
            string = "jedovcela    "
            y = x >> 8
            show_string(string[:y])
        #time.sleep_us(50)
        show_number1(time.localtime()[4]*100 +time.localtime()[5])    
