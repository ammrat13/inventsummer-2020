import copy
from enum import Enum
import json
import math
import numpy as np
import scipy.integrate

from lib.animate import animate
import lib.constants as constants
from lib.utilities import merge_dicts
from lib.world import World
from my_bang_bang_controller import BangBangController

CRUISE_CONTROL_TEST = 'tests/step-input.json'


class ExitStatus(Enum):
    """ Exit status values indicate the reason for simulation termination. """
    COMPLETE = 'SUCCESS: End reached.'
    TIMEOUT = 'TIMEOUT: Simulation end time reached.'
    INF_VALUE = 'ERROR: Your controller returned a command of inf.'
    NAN_VALUE = 'ERROR: Your controller returned a command of nan.'


def simulate_cruise_control(controller, hill=False):
    # Setup
    car = Car(constants.CAR_MASS)
    traj = Reference(CRUISE_CONTROL_TEST, offset=car.length/2)
    if hill:
        world = World(constants.HILL_SLOPE, hill=True)
    else:
        world = World(constants.GROUND_HEIGHT)

    # Simulate and animate
    results = simulate(car, world, traj, controller, slope=hill)
    animate(world, [results])

    return results


def simulate(car, world, trajectory, controller, sampling_period=.1, drag=True, slope=False, terminate=None):
    """
    Perform a simulation of the car and return the numerical results.

    Inputs:
        car, Car object
        world, a world object
        controller, Controller object
        trajectory, Reference object
        terminate, None, False, or a function of time and state that returns
            ExitStatus. If None (default), terminate when hover is reached at
            the location of trajectory with t=t_final. If False, never terminate
            before timeout or error. If a function, terminate when returns not
            None.

    Outputs:
        results, a dictionary with the following keys
            time, seconds, shape=(N,)
            state, a dict describing the state history with keys
                x, position, m
                v, linear velocity, m/s
            control, an array describing the command input history
            output, an array describing the desired outputs from the trajectory
            exit_status, an ExitStatus enum indicating the reason for termination.
    """

    # determine initial state of car
    initial_state = {'x': trajectory.waypoints['x'][0], 'v': trajectory.waypoints['v'][0]}

    if terminate is None:  # Default exit terminate at final position of trajectory
        normal_exit = traj_end_exit(initial_state, trajectory)
    elif terminate is False:  # Never exit before timeout.
        normal_exit = lambda t, s: None
    else:  # Custom exit.
        normal_exit = terminate

    time = [0]
    state = [copy.deepcopy(initial_state)]
    reference = [trajectory.update(time[-1])]
    control = [controller.update(sampling_period, state[-1], reference[-1])]

    exit_status = None
    while True:
        exit_status = exit_status or safety_exit(state[-1], control[-1])
        # exit_status = exit_status or normal_exit(time[-1], state[-1])
        exit_status = exit_status or time_exit(time[-1], trajectory.t_final)
        if exit_status:
            break
        time.append(time[-1] + sampling_period)
        state.append(car.step(state[-1], control[-1], sampling_period, drag, slope))
        reference.append(trajectory.update(time[-1]))
        control.append(controller.update(sampling_period, state[-1], reference[-1]))

    # return information packed into results dict
    results = dict(time=np.array(time, dtype=float),
                   state=merge_dicts(state),
                   control=control,
                   reference=reference,
                   exit_status=exit_status)
    return results


def traj_end_exit(initial_state, trajectory):
    """
    Returns a exit function. The exit function returns an exit status message if
    the car is at end of the provided trajectory. If the
    initial state is already at the end of the trajectory, the simulation will
    run for at least one second before testing again.
    """

    xf = trajectory.update(np.inf)
    if np.array_equal(initial_state['x'], xf):
        min_time = 1.0
    else:
        min_time = 0

    def exit_fn(time, state):
        # Success is reaching near-zero speed with near-zero position error.
        if time >= min_time and state['x'] - xf < 0.02 and state['v'] <= 0.02:
            return ExitStatus.COMPLETE
        return None

    return exit_fn


def time_exit(time, t_final):
    """
    Return exit status if the time exceeds t_final, otherwise None.
    """
    if time >= t_final:
        return ExitStatus.TIMEOUT
    return None


def safety_exit(state, control):
    """
    Return exit status if any safety condition is violated, otherwise None.
    """
    if np.any(np.isinf(control)):
        return ExitStatus.INF_VALUE
    if np.any(np.isnan(control)):
        return ExitStatus.NAN_VALUE
    return None


class Car(object):
    """
    Car dynamics model
    """

    def __init__(self, mass):
        """
        Initialize Car's physical and dynamical parameters

        Input
            mass, mass in kilograms of the car
        """

        self.mass = mass  # kg
        self.u_max = constants.MAX_POWER # maximum power provided by the car's engine, W/s
        self.Cd = .275  # nominal drag coefficient for a car, unitless
        self.A = 1.6 + 0.00056 * (mass - 765)  # cross sectional area as function of mass, m^2
        self.rho = 1.225  # air density (kg/m^3)
        self.length = 7.5  # m
        self.height = 1.2  # m

    def step(self, state, command, t_step=0.1, drag=False, slope=False):
        """
        Integrate dynamics forward from state given constant input for time t_step.

        Input
            state, state dictionary of the current state of the car
            command, input command to perform zero order hold over the t_step
            t_step, amount of time to integrate input over
            drag, boolean turning on effect of drag on the car
            slope, boolean turning on effect of road grade on the car

        Output
            dictionary of state after integration
        """

        # Define anonymous function that can be used by the integrator
        def _s_dot(t, s): return self._s_dot_fn(t, s, command, drag, slope)

        # Solve initial value problem
        s = self._pack_state(state)
        sol = scipy.integrate.solve_ivp(_s_dot, (0, t_step), s, first_step=t_step)
        s = sol.y[:, -1]
        return self._unpack_state(s)

    def _s_dot_fn(self, t, s, F, drag, slope):
        """
        Compute derivative of state for Car given fixed control inputs as
        an autonomous ODE.

        Input
            t, current time in simulation
            s, packed form of current state
            F, current force acting on vehicle
            drag, boolean turning on drag forces
            slope, boolean turning on road grade forces

        Output
            packed vector of state derivative
        """
        # Unpack state information
        state = self._unpack_state(s)

        # Position derivative
        x_dot = max(state['v'], 0.0)

        # Velocity derivative
        F_sum = F
        if drag:
            F_sum -= 0.5 * self.rho * self.Cd * self.A * x_dot ** 2
        if slope:
            F_sum -= self.mass * constants.GRAVITY * math.sin(math.atan(constants.HILL_SLOPE))

        v_dot = F_sum / self.mass

        # Pack into vector of derivatives
        return np.array([x_dot, v_dot])

    @staticmethod
    def _pack_state(state):
        """
        Convert a state dict to Car's private internal vector representation

        Input
            state, the expanded state in dictionary form

        Output
            s, the packed state in array form
        """
        return np.array([state['x'], state['v']])

    @staticmethod
    def _unpack_state(s):
        """
        Convert Car's private internal vector representation to a state dict.

        Input
            s, the packed state in array form

        Output
            state, the expanded state in dictionary form
        """
        return {'x': s[0], 'v': max(s[1], 0.0)}  # Make sure we don't go backwards


class Reference(object):
    """
    Reference class to store information about reference data
    """

    def __init__(self, data, offset=0):
        """
        Initialize a trajectory from either a filename or a results dictionary generated from a simulation

        Inputs,
            data, source to draw info from
            offset, starting distance to offset leader relative to followe, defaults to 0
        """
        if type(data) is dict:
            self.waypoints = dict(x=data['state']['x'][0] + [offset],
                                  v=data['state']['v'],
                                  t=data['time'])
            self.t_final = data['time'][-1]
        elif type(data) is str and data.endswith('.json'):
            with open(data) as file:
                data = json.load(file)
            self.waypoints = data['waypoints']
            self.waypoints['x'][0] += offset
            self.t_final = data['t_final']
        else:
            print("Error: Received unexpected data type as argument. "
                  "Pass in the path to a .json file or a simulation results dictionary.")

    def update(self, t):
        """
        Given a timestamp, evaluate the Reference at this point and return the desired velocity
        """
        for i in range(len(self.waypoints['t'])):
            if t < self.waypoints['t'][i]:
                return self.waypoints['v'][i - 1]
        return self.waypoints['v'][-1]
