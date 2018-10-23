#import RPi.GPIO as GPIO
from time import sleep as sleep
from timeit import default_timer as timer


class LEDboard:

    _pins = [5, 6, 13]

    _pin_led_states = [
        [1, 0, -1],  # A
        [0, 1, -1],  # B
        [-1, 1, 0],  # C
        [-1, 0, 1],  # D
        [1, -1, 0],  # E
        [0, -1, 1]   # F
        ]

    #GPIO.setmode(GPIO.BCM)

    def turn_off_all(self):
        GPIO.setup(0, GPIO.IN)
        GPIO.setup(1, GPIO.IN)
        GPIO.setup(2, GPIO.IN)

    def set_pin(self, pin_index, pin_state):
        if pin_state == -1:
            GPIO.setup(self._pins[pin_index], GPIO.IN)
        else:
            GPIO.setup(self._pins[pin_index], GPIO.OUT)
            GPIO.output(self._pins[pin_index], pin_state)

    def light_led(self, led_number):
        for pin_index, pin_state in enumerate(self._pin_led_states[led_number]):
            self.set_pin(pin_index, pin_state)

    def proxy_light_led(self, i):
        #i = 1
        print(i)

    def power_down(self):  # Log out
        leds_on = 6
        while leds_on > 0:
            print("number of leds: " + str(leds_on))
            start = timer()
            end = timer()
            while (end - start) < 1:
                for i in range(leds_on):
                    self.light_led(i)
                end = timer()
            leds_on = leds_on - 1
        self.turn_off_all()

    def power_up(self):  # First key pressed
        leds_on = 1
        while leds_on < 7:
            print("number of leds: " + str(leds_on))
            start = timer()
            end = timer()
            while (end - start) < 1:
                for i in range(leds_on):
                    # self.light_led(i)
                    self.proxy_light_led(i)
                end = timer()
            leds_on = leds_on + 1
        self.turn_off_all()

    def turn_on_led(self, led_number, sec):  # Turn on a specific led for sec seconds
        self.light_led(led_number)
        start = timer()
        end = timer()
        while (end - start) < sec:
            end = timer()
        self.turn_off_all()

    def flash_all_leds(self, sec):  # If user enters wrong password
        start = timer()
        now = timer()
        while (now - start) < sec:
            flash_change = timer()
            while (now - flash_change) < 0.5:
                for i in range(6):
                    #self.light_led(i)
                    self.proxy_light_led(i)
                now = timer()
            self.turn_off_all()
            sleep(0.5)
            now = timer()

    def twinkle_all_leds(self, sec):  # if user enters password successfully
        start = timer()
        now = timer()
        while (now - start) < sec:
            for i in range(6):
                self.light_led(i)
                sleep(0.2)
            now = timer()
        self.turn_off_all()