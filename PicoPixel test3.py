#import machine
from machine import Pin, PWM
import utime

c1 = machine.Pin(5, machine.Pin.OUT)
c2 = machine.Pin(6, machine.Pin.OUT)
c3 = machine.Pin(7, machine.Pin.OUT)
c4 = machine.Pin(8, machine.Pin.OUT)
sleep=0.001
sleep2=0.1

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

rows_latch = machine.Pin(19, machine.Pin.OUT)
rows_data = machine.Pin(18, machine.Pin.OUT)
rows_clock = machine.Pin(17, machine.Pin.OUT)
cols_latch = machine.Pin(22, machine.Pin.OUT)
cols_data = machine.Pin(21, machine.Pin.OUT)
cols_clock = machine.Pin(20, machine.Pin.OUT)

chars = {
    #      a  b  c  d  e  f  g  dp
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
    #     a  b  c  d  e  f  g  dp
    "0": [1, 1, 1, 1, 1, 1, 0, 0],
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
    }

cols1 = [
    #    1. 2. 3. 4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32
      [0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
      [0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
      [1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
      [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
      [0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      [0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    ]
cols2 = [
    #    1. 2. 3. 4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32
      [0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
cols3= [
    "   %                            ",
    "                                ",
    "         %                      ",
    "                                ",
    "                 %              ",
    "                                ",
    "                 %              ",
    "                        %%      ",

    ]

cols4= [
"10000010000000000100001111111110",
"11000011101111000000111101111000",
"11000000111100011111101110011110",
"11011110000000000001110100111111",
"11011110111111111111100001111111",
"11000000000000011100001001111111",
"11110001111111000001111110001000",
"10000111111111111111111111111111",


    ]


def seg_print(segment): #print one segment - a,b,c,d,e,f,g,dp
    vals = chars[segment]
    for segment_number in range(0, 8):
        segment_pins[segment_number].value(vals[segment_number])


def seg_print_letter(letter):
    vals = letters[letter]
    for segment_number in range(0, 8):
        segment_pins[segment_number].value(vals[segment_number])


def matrix_latch(): #"obnoví" obraz
    cols_latch.value(1)
    cols_latch.value(0)
    rows_latch.value(1)
    rows_latch.value(0)


def matrix_clear(): #nastaví všechny body matrixu na 0
    for col in range(0, 32):
        cols_data.value(1)
        cols_clock.value(1)
        cols_clock.value(0)
    for row in range(0, 8):
        rows_data.value(0)
        rows_clock.value(0)
        rows_clock.value(1)
    matrix_latch()


def matrix_write(data):
    cols_data.value(0)
    cols_clock.value(1)
    cols_data.value(1)
    for x in range(0, 32, 1):
        for y in range(7, -1, -1): # iteruje od 7mi k nule
            vals = (data)[y]
            rows_data.value(vals[x])
            rows_clock.value(0)
            rows_clock.value(1)
        cols_clock.value(1)
        cols_clock.value(0)
        matrix_latch()
        # utime.sleep(0.1)
    matrix_clear()


def matrix_write1(data):
    cols_data.value(0)
    cols_clock.value(1)
    cols_data.value(1)
    for x in range(0, 32, 1):
        for y in range(7, -1, -1): # iteruje od 7mi k nule
            vals = (data)[y]
            rows_data.value(1 if vals[x]!=" "and vals[x]!="0"else 0)
            rows_clock.value(0)
            rows_clock.value(1)
        cols_clock.value(1)
        cols_clock.value(0)
        matrix_latch()
        # utime.sleep(0.1)
    matrix_clear()


def matrix_push_col():
    cols_data.value(1)
    cols_clock.value(1)
    cols_clock.value(0)
    matrix_latch()


def matrix_push_row():
    rows_data.value(0)
    rows_clock.value(1)
    rows_clock.value(0)
    matrix_latch()



while True:

    c1.value(1)
    c2.value(0)
    c3.value(0)
    c4.value(0)
    seg_print_letter("a")
    utime.sleep(sleep)
    c1.value(0)
    c2.value(1)
    c3.value(0)
    c4.value(0)
    seg_print_letter("c")
    utime.sleep(sleep)
    c1.value(0)
    c2.value(0)
    c3.value(1)
    c4.value(0)
    seg_print_letter("2")
    utime.sleep(sleep)
    c1.value(0)
    c2.value(0)
    c3.value(0)
    c4.value(1)
    seg_print("a")
    utime.sleep(sleep)

    while button6.value():
        # relay.freq(8)
        # relay.duty_u16(30000)

        for x in range(0, 1):
            cols_data.value(0)
            cols_clock.value(1)
            cols_clock.value(0)
            cols_latch.value(1)
            cols_latch.value(0)


        for x in range(0, 1):
            rows_data.value(1)
            rows_clock.value(0)
            rows_clock.value(1)
            rows_latch.value(1)
            rows_latch.value(0)

        utime.sleep(0.1)

    if not button6.value():
        relay.duty_u16(0)

    if button2.value():
        # relay.freq(70)
        # relay.duty_u16(30000)
        matrix_clear()
        # utime.sleep(0.1)

    if button4.value():
        # relay.freq(70)
        # relay.duty_u16(30000)
        # matrix_push_col()
        matrix_write1(cols4)
        # utime.sleep(0.1)

    if button5.value():
        # relay.freq(70)
        # relay.duty_u16(30000)
        matrix_push_row()
        utime.sleep(0.1)

    if button1.value():
        matrix_write(cols1)
        # utime.sleep(0.1)
    if button3.value():
        matrix_write(cols2)

