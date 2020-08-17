from abc import ABC, abstractmethod
import numpy as np

import lib.constants as constants


class Controller(ABC):

    def update(self, dt, state, ref):
        command = self.controller(dt, state, ref)
        command_clipped = np.clip(command, -constants.MAX_POWER, constants.MAX_POWER)
        return command_clipped

    @abstractmethod
    def controller(self, dt, state, ref):
        pass
