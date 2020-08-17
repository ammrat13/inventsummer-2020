import lib.constants as constants  # Useful parameters
import lib.controller_super as controller_super  # Super class with controller API


class PIDController(controller_super.Controller):

    def __init__(self):
        self.prev_state = None
        self.error_int = 0.0

    def controller(self, dt, state, ref):
        # Constants
        KP = 2000
        KI = 8
        KD = 1200
        # First iteration - check for derivative calculation
        if self.prev_state == None:
            self.prev_state = state
        # Integrate
        self.error_int += dt * (state['v'] - ref)
        # Compute the terms
        p = -KP * (state['v'] - ref)
        i = -KI * self.error_int
        d = -KD * (state['v'] - self.prev_state['v']) / dt
        # Advance the stored state
        self.prev_state = state
        # Return
        return p + i + d
