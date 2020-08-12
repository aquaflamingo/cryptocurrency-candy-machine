from gpiozero import Servo
from time import sleep

def execute():
    gpio=17
    servo = Servo(gpio)
    print("Airdrop initiated!")
    i=1
    while i in range(1,4):
            servo.mid()
            sleep(1)
            i = i+1
    print("Done.. Enjoy!")
    return
