import RPi.GPIO as GPIO
import time


class Keypad:

    # Global variables
    keypad_matrix = [[1,2,3],
                     [4,5,6],
                     [7,8,9],
                     ['*',0,'#']]
    ROW = [18,23,24,25]
    COL = [17,27,22]

    def setup(self):
        GPIO.setmode(GPIO.BCM)

        #Declaring rowpins as output
        for rp in range(4):
            GPIO.setup(ROW[rp], GPIO.OUT)
            #GPIO.output(ROW[rp], 1)

        """
        GPIO.setup(18, GPIO.OUT)        #R0
        GPIO.setup(23, GPIO.OUT)        #R1
        GPIO.setup(24, GPIO.OUT)        #R2
        GPIO.setup(25, GPIO.OUT)        #R3
        """

        #Declaring columnpins as input,
        #   GPIO.PUD_DOWN declares that pin will employ a pull-down resistor
        for cp in range(3):
            GPIO.setup(ROW[cp], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


        """
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)         #C0
        GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)         #C1
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)         #C2

        """


    #Keypad object serves as an interface between agent and physical keypad,
    #   its job is to poll the keypad to detect keystrokes and send these to the agent
    def do_polling(self):
        try:
            while True:
                for rp in ROW:
                    GPIO.output(ROW[rp], GPIO.HIGH)                 #Sets rowpin high one at a time
                    for cp in COL:
                        if GPIO.input(cp) == GPIO.HIGH:             #Checks if rowpin is high
                            pressed_key = keypad_matrix[rp][cp]
                            print("Key pressed: ", pressed_key)
                            return pressed_key                      #Returns pressed symbol
                        else:
                            pass
                            #print("No key has been pressed.")
                        time.sleep(0.01)
                    GPIO.output(ROW[rp], GPIO.LOW)                  #Resets rowpin
        except KeyboardInterrupt:
            GPIO.cleanup()



    def get_next_signal(self):
        pressed_key = 0
        while pressed_key == 0:
            self.do_polling()