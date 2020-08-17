import lib.constants as constants  # Useful parameters
import lib.controller_super as controller_super  # Super class with controller API


class PController(controller_super.Controller):

    def controller(self, dt, state, ref):
        return -1000 * (state['v'] - ref)
