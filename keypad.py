#import RPi.GPIO as GPIO
import time
#GPIO.setwarnings(False)

class Keypad:

    def __init__(self):
        self.keypad_matrix = [[1, 2, 3],
                              [4, 5, 6],
                              [7, 8, 9],
                              ['*', 0, '#']]

        self.row_pins = [18, 23, 24, 25]
        self.col_pins = [17, 27, 22]
        self.pressed_key = None
        self.setup()


    def setup(self):
        GPIO.setmode(GPIO.BCM)
        # Declaring rowpins as output
        for rp in self.row_pins:
            GPIO.setup(rp, GPIO.OUT)

        for cp in self.col_pins:
            GPIO.setup(cp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    #Keypad object serves as an interface between agent and physical keypad,
    #   its job is to poll the keypad to detect keystrokes and send these to the agent
    def do_polling(self):
        for rp in range(4):
            GPIO.output(self.row_pins[rp], GPIO.HIGH)                 #Sets rowpin high one at a time
            for cp in range(3):
                if GPIO.input(self.col_pins[cp]) == GPIO.HIGH:             #Checks if rowpin is high
                    print(rp, cp)
                    self.pressed_key = self.keypad_matrix[rp][cp]
                    print("Key pressed: ", self.pressed_key)
                    GPIO.output(self.row_pins[rp], GPIO.LOW)
                    return self.pressed_key                      #Returns pressed symbol
                time.sleep(0.01)
            GPIO.output(self.row_pins[rp], GPIO.LOW)    #Resets rowpin



    def get_next_signal(self):
        try:
            while True:
                signal = self.do_polling()
                if signal:
                    print("Next signal: ", signal)
                    return signal
        except KeyboardInterrupt:
            GPIO.cleanup()