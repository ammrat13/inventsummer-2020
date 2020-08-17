import lib.constants  as constants  # Useful parameters
import lib.controller_super as controller_super  # Super class with controller API


class BangBangController(controller_super.Controller):

    def controller(self, dt, state, ref):
        if state['v'] < ref:
            return constants.MAX_POWER
        elif state['v'] > ref:
            return -constants.MAX_POWER
        else:
            return 0.0
