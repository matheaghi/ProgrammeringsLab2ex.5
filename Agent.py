from inspect import isfunction

class KPC:
    def __init__(self):
        self.keypad = None
        self.ledBoard = None
        self.password = None
        self.CUMP = None
        self.old_CUMP = None
        self.override = None
        self.lid = None
        self.ldur = None

    def intit_passcode_entry(self):
        return None

    def get_next_signal(self):
        return None

    def verify_login(self):
        return None

    def verify_passcode_change(self):
        return None

    def light_one_led(self):
        return None

    def flash_leds(self):
        return None

    def twinkle_leds(self):
        return None

    def exit_action(self):
        return None



class FSM:
    def __init__(self):
        return None

    def add_rule(self):
        return None

    def get_next_signal(self):
        return None

    def run_rules(self):
        return None

    def apply_rule(self):
        return None

    def fire_rule(self):
        return None

    def main_loop(self):
        return None

