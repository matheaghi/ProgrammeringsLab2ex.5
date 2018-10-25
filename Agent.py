from inspect import isfunction
import time
import keypad
import Led

class KPC:
    def __init__(self):
        self.keypad = keypad.Keypad()
        self.ledBoard = Led.LEDboard()
        self.CUMP = ""
        self.override = '0'
        self.lid = ""
        self.ldur = ""
        self.mock = ['8', '1', '2', '3', '4', '5', '*', '4', '*', '2', '9', '*', '2', '*', '1', '4', '*', '#', '#']
        self.mock2 = ['8', '1', '2', '3', '4', '5', '*', '*', '5', '4', '3', '2', '1', '*']
        self.mock_counter = 0

        f = open("passcode.txt", "r")
        self.password = f.readline()
        print(self.password)
        f.close()


    def intit_passcode_entry(self, symbol):
        self.ledBoard.power_up()
        #print("Power up")

    def get_next_signal(self):

        if (self.override != '0'):
            ret = self.override
            self.override = '0'
            return ret
        else:
            return str(self.keypad.get_next_signal())

    def verify_login(self, symbol):
        print("Verify login: " + str(self.CUMP))
        if (self.CUMP == self.password):
            self.CUMP = ""
            self.override = "Y"
            print("Y")
            print(self.override)
        else:
            self.CUMP = ""
            self.override = "N"
            print("0")

    def verify_passcode_change(self, symbol):
        if(self.password_is_number(self.CUMP) and (len(self.CUMP) >= 4)):
            self.set_new_password(self.CUMP)
            self.CUMP = ""
            #print("Password verified")
        else:
            self.CUMP = ""

    def password_is_number(self, password):
        fsm = FSM()
        numbers = 0
        for i in password:
            if(fsm.signal_is_digit(i)):
                numbers += 1
        if(numbers == len(password)):
            return True
        return False

    def light_one_led(self, symbol):
        self.ledBoard.turn_on_led(int(self.lid), int(self.ldur))
        #print("Turn on led nr " + self.lid + " for " + self.ldur + " seconds.")
        self.clearAll(symbol)

    def flash_leds(self, symbol):
        self.ledBoard.flash_all_leds(2)
        self.CUMP = ""
        #print("Flash leds")

    def twinkle_leds(self, symbol):
        self.CUMP = ""
        self.ledBoard.twinkle_all_leds(2)
        #print("Twinkle leds")

    def exit_action(self, symbol):
        self.ledBoard.power_down()
        #print("Power down")
        self.clearAll(symbol)

    def do_nothing(self, symbol):
        return None

    def add_to_CUMP(self, symbol):
        #print("symbol: " + str(symbol))
        self.CUMP += symbol
        #print("CUMP: " + str(self.CUMP))

    def set_lid(self, symbol):
        self.lid = symbol

    def set_ldur(self, symbol):
        self.ldur += symbol

    def set_new_password(self, password):
        f = open("passcode.txt", "r+")
        f.truncate(0)
        f.close()
        f = open("passcode.txt", "w")
        f.write(password)
        f.close()
        self.password = password

    def clearAll(self, symbol):
        self.CUMP = ""
        self.lid = ""
        self.ldur = ""

    def mock_next_symbol(self):
        if (self.override != '0'):
            ret = self.override
            self.override = '0'
            return ret
        else:
            self.mock_counter += 1
            return self.mock[self.mock_counter-1]





class FSM:
    def __init__(self):
        self.state = 0
        self.signal = '0'
        self.kpc = KPC()
        self.rbs = []


    def signal_is_digit(self, signal): return 48 <= ord(signal) <= 57
    def any_symbol(self, signal): return True

    def add_rule(self, st1, st2, signal, action):
        rule = Rule(st1, st2, signal, action)
        self.rbs.append(rule)

    def get_next_signal(self):
        return self.kpc.get_next_signal()

    def mock_next_symbol(self):
        return self.kpc.mock_next_symbol()

    def run_rules(self):
        print("run rules")
        for rule in self.rbs:
            if(isfunction(rule.signal) == False):
                if (rule.state1 == self.state and ((rule.signal == self.signal) or (rule.signal == True))):
                    self.state = rule.state2
                    rule.action(self.signal)
                    break
            elif(isfunction(rule.signal)):
                if(rule.state1 == self.state and rule.signal(self.signal) == self.signal):
                    self.state = rule.state2
                    rule.action(self.signal)
                    break

    def main_loop(self):
        print("You have moved to state: " + str(self.state))
        self.signal = self.get_next_signal()
        print("Symbol in is: " + str(self.signal))
        self.run_rules()
        time.sleep(1)



class Rule:
    def __init__(self, st1, st2, signal, action):
        self.state1 = st1
        self.state2 = st2
        self.signal = signal
        self.action = action

if __name__ == '__main__':

    kpc = KPC()
    fsm = FSM()

    fsm.add_rule(0, 1, fsm.any_symbol(fsm.signal), fsm.kpc.intit_passcode_entry)
    fsm.add_rule(1, 2, '*', fsm.kpc.verify_login)
    fsm.add_rule(1, 1, fsm.signal_is_digit(fsm.signal), fsm.kpc.add_to_CUMP)
    fsm.add_rule(1, 0, fsm.any_symbol(fsm.signal), fsm.kpc.flash_leds)
    fsm.add_rule(2, 3, "Y", fsm.kpc.twinkle_leds)
    fsm.add_rule(2, 1, fsm.any_symbol(fsm.signal), fsm.kpc.flash_leds)
    fsm.add_rule(3, 4, "*", fsm.kpc.do_nothing)
    fsm.add_rule(3, 8, "#", fsm.kpc.do_nothing)
    fsm.add_rule(3, 6, fsm.signal_is_digit(fsm.signal), fsm.kpc.set_lid)
    fsm.add_rule(4, 3, "*", fsm.kpc.verify_passcode_change)
    fsm.add_rule(4, 4, fsm.signal_is_digit(fsm.signal), fsm.kpc.add_to_CUMP)
    fsm.add_rule(6, 7, "*", fsm.kpc.do_nothing)
    fsm.add_rule(6, 3, fsm.any_symbol(fsm.signal), fsm.kpc.clearAll)
    fsm.add_rule(7, 3, '*', fsm.kpc.light_one_led)
    fsm.add_rule(7, 7, fsm.signal_is_digit(fsm.signal), fsm.kpc.set_ldur)
    fsm.add_rule(7, 3, fsm.any_symbol(fsm.signal), fsm.kpc.clearAll)
    fsm.add_rule(8, 0, "#", fsm.kpc.exit_action)
    fsm.add_rule(8, 3, fsm.any_symbol(fsm.signal), fsm.kpc.clearAll)

    while True:
        fsm.main_loop()
