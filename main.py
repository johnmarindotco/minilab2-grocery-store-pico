import time
time.sleep(0.1) # Wait for USB to become ready

print("Hello, Pi Pico!")

from machine import *
from Buzzer import *
from LightStrip import *
from Displays import *
from Button import *
from modelclasses import *
from Sensors import *
import time

sensor = Pin(9, Pin.IN, Pin.PULL_UP)
prox = DigitalSensor(pin=6, name='Prox')

while True:
    val = sensor.value()
    if val == 0:
        prox.tripped()
        print("sensor has been tripped.")
    else:
        prox.tripped()
        print("sensor not currently tripped.")
    time.sleep(0.8)


class DigitalPriceDisplay:
    def __init__(self):
        self.buzzer = PassiveBuzzer(pin=28, name='Buzz')
        self.lightstrip = LightStrip(pin=22, name='Lights')
        self.display = LCDDisplay(sda=0, scl=1)
        self.leftbutton = Button(pin=19, name="left", handler=self)
        self.rightbutton = Button(pin=11, name="right", handler=self)
        self.myproducts = []
        self.addProducts()
        self.index = 0

        self.led1 = Pin(13, Pin.OUT)
        self.led1.value(0)

        self.led2 = Pin(14, Pin.OUT)
        self.led2.value(0)

    def addProducts(self):
        product1 = PackagedProduct('1234', 'Oatmeal', 'Organic Oatmeal', 100, 'GM', 2.50)
        product2 = PackagedProduct('1234', 'Cereal', 'Froot Loops', 10, 'GM', 1.49)
        product3 = PackagedProduct('1234', 'Oatmeal', 'Organic Oatmeal', 100, 'GM', 2.50)
        product4 = PackagedProduct('1234', 'Cereal', 'Froot Loops', 10, 'GM', 1.49)
        self.myproducts.append(product1)
        self.myproducts.append(product2)
        self.myproducts.append(product3)
        self.myproducts.append(product4)

    def showInfo(self):
        self.display.clear()
        currentproduct = self.myproducts[self.index]
        self.display.showText(currentproduct.line1(), 0)
        self.display.showText(currentproduct.line2(), 1)
        self.display.showText(currentproduct.line1(), 2)
        self.display.showText(currentproduct.line2(), 3)

    def previousProduct(self):
        if self.index > 0:
            self.index = self.index - 1
            self.showInfo()
        self._blink_red_led()
        self.buzzer.beep(tone=500)

    def nextProduct(self):
        if self.index < len(self.myproducts) -1:
            self.index = self.index + 1
            self.showInfo()
        self._blink_green_led()
        self.buzzer.beep(tone=1000)

    def buttonPressed(self, name):
        if name == 'left':
            self.previousProduct()
        else:
            self.nextProduct()

    def buttonReleased(self, name):
        pass

    def _blink_red_led(self):
        self.led1.value(1)
        time.sleep(1)
        self.led1.value(0)

    def _blink_green_led(self):
        self.led2.value(1)
        time.sleep(1)
        self.led2.value(0)

    def _blink_light(self, times=3, interval=0.15):
        try:
            self.lightstrip.blink(times=times, interval=interval)
            return
        except AttributeError:
            pass

        if hasattr(self.lightstrip, "on") and hasattr(self.lightstrip, "off"):
            for _ in range(times):
                self.lightstrip.on()
                time.sleep(interval)
                self.lightstrip.off()
                time.sleep(interval)
            return

        on_color = (255, 255, 255)
        has_fill  = hasattr(self.lightstrip, "fill")
        has_show  = hasattr(self.lightstrip, "show")
        has_clear = hasattr(self.lightstrip, "clear")

        if has_fill and (has_show or has_clear):
            for _ in range(times):
                self.lightstrip.fill(on_color)
                if has_show:
                    self.lightstrip.show()
                time.sleep(interval)
                if has_clear:
                    self.lightstrip.clear()
                else:
                    self.lightstrip.fill((0, 0, 0))
                if has_show:
                    self.lightstrip.show()
                time.sleep(interval)
            return

        print("Light blink skipped")


if __name__ == '__main__':
    myDisplay = DigitalPriceDisplay()
    myDisplay.showInfo()

    # loop for keeping session open for visual studio
    while True:
        time.sleep(1)
