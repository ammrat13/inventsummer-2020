from lib.simulator import simulate_cruise_control
from lib.utilities import plot
"""
Import your controller here.
"""
from my_pid_controller import PIDController

"""
Instantiate your controller here.
"""
controller = PIDController()

"""
Run simulation of cruise control scenario.
"""
results = simulate_cruise_control(controller, hill=True)

"""
Plot the results!
"""
# Plotting example
plot(results['time'], [results['reference']],
     [results['state']['v']],
     xlabel="Time (s)",
     ylabels=["Set Point (m/s)", "Velocity (m/s)"])
