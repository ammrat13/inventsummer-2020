import math
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from scipy import ndimage

import lib.constants as constants

MAX_POWER = constants.MAX_POWER / 100  # Div by 100 for percent throttle


class Car:
    """
    class to create Car shape for animation
    """

    def __init__(self, frames, state, control, reference, world, color='s'):
        """
        Initialize a Car object in the animation.

        Parameters
            frames, array of times the simulation is sampled for
            state, dictionary containing state information with keys
                x, an array of the position of the car at sampled frames
                v, an array of the velocity of the car at sampled frames
        """
        # Supersample states
        i, remainder = np.divmod(frames, 1)
        self.x = state['x'][i.astype(int)] + remainder * (state['x'][(i + 1).astype(int)] - state['x'][i.astype(int)])
        self.v = state['v'][i.astype(int)] + remainder * (state['v'][(i + 1).astype(int)] - state['v'][i.astype(int)])

        # Supersample control command
        command = control[i.astype(int)] + remainder * (control[(i + 1).astype(int)] - control[i.astype(int)])
        self.brake = [c if c < 0 else 0 for c in command]
        self.throttle = [c if c > 0 else 0 for c in command]

        # Supersample reference
        self.ref = reference[i.astype(int)] + remainder * (reference[(i + 1).astype(int)] - reference[i.astype(int)])

        # Define car artist
        if world.is_hill:
            angle = math.degrees(math.atan(constants.HILL_SLOPE)) * 2.3
            out = ndimage.rotate(plt.imread('lib/art/' + color + '.png'), angle)
            img = (out * 255).astype(np.uint8)
        else:
            img = plt.imread('lib/art/' + color + '.png')
        imagebox = OffsetImage(img, zoom=.1)
        self.artist = AnnotationBbox(imagebox, [0, 0], boxcoords='offset points', frameon=False)

        # Save world information
        self.ground = world.f

    def draw(self, frame):
        """
        Redraw the Car object in the animation

        Parameters
            frame, frame number of animation to render
        """
        x = self.x[frame]
        self.artist.xy = [x, self.ground(x) + .6]  # half the car height is added
        return self.x[frame]


def animate(world, results):
    """
    Animate a completed simulation result based on the time and position.
    The animation may be viewed live or saved to a .mp4 video (slower, requires additional libraries).

    Inputs
        world, a World object
        results, (N,) an array of simulation results dictionaries\

    Output
        an animation
    """

    # Style parameters
    rtf = 1.0  # real time factor > 1.0 is faster than real time playback
    render_fps = 10
    width = 30
    height = 10
    start_x = -5
    ytick_spacing = 2
    xtick_spacing = 10
    colors = ['b', 'o', 'r', 'g', 's', 'y']

    # Supersample timestamps through interpolation to render interval; always include t=0
    time = results[0]['time']
    frames = np.interp(np.arange(0, time[-1], 1 / render_fps * rtf), time, np.arange(time.size))

    # Create objects
    cars = [Car(frames, results[i]['state'], np.asarray(results[i]['control'])/MAX_POWER, np.asarray(results[i]['reference']), world, colors[i]) for i in range(len(results))]

    # Set up plot
    if len(cars) <= 1:
        fig = plt.figure('Cruise Control Simulation', figsize=(10,8))
        ax = fig.add_subplot(111, autoscale_on=False, xlim=(start_x, width + start_x), ylim=(0, height))
        car_text = ax.text(0, height-1.5, '', bbox={'facecolor': 'blue', 'alpha': 0.25, 'pad': 10})
    else:
        fig = plt.figure('Adaptive Cruise Control Simulation', figsize=(10,8))
        ax = fig.add_subplot(111, autoscale_on=False, xlim=(start_x, width + start_x), ylim=(0, height))
        car_text = ax.text(0, height-2.0, '', bbox={'facecolor': 'orange', 'alpha': 0.25, 'pad': 10})
    ground, = ax.plot([], [], 'k', lw=5)
    yticks = np.arange(0, np.ceil(np.max([world.f(car.x[-1]) for car in cars]) + height), ytick_spacing)
    xticks = np.arange(0, np.ceil(np.max([car.x[-1] for car in cars]) + width), xtick_spacing)
    ax.grid()

    # Initialize function to initialize the animation call
    def initialize():
        ground.set_data([], [])
        car_text.set_x(0)
        [ax.add_artist(car.artist) for car in cars]
        return ground, [car.artist for car in cars]

    # Updating function, to be repeatedly called by the animation
    def update(frame):
        ref = [car.ref[frame] for car in cars]
        position = np.array([car.draw(frame) for car in cars])
        speeds = [car.v[frame] for car in cars]
        throttles = [car.throttle[frame] for car in cars]
        brakes= [car.brake[frame] for car in cars]
        left_x = max(start_x, np.average(position) - (width / 2))
        x = np.linspace(left_x, left_x + width, 100)
        y = world.f(x)
        ax.set_xlim(left_x, left_x + width)
        ax.xaxis.set_ticks(xticks[np.where(np.logical_and(xticks >= left_x, xticks <= left_x + width))])
        ground.set_data(x, y)
        car_text.set_x(left_x+1)
        car_text.set_x(left_x+1)
        if world.is_hill:
            ax.set_ylim(y[0], y[0] + height)
            ax.yaxis.set_ticks(yticks[np.where(np.logical_and(yticks >= y[0], yticks <= y[0] + height))])
            car_text_y_offset = 1.5 if len(cars) <= 1 else 2.0
            car_text.set_y(y[0] + height - car_text_y_offset)
            ax.fill_between(x, y, -10*np.ones(len(y)), facecolor='g')
        else:
            ax.fill_between(x, y, facecolor='g')
        if len(cars) <= 1:  # cruise control text
            car_text.set_text('Speed Set Point: {:>5.2f} m/s\nCurrent Speed: {:>5.2f} m/s\nThrottle: {:>5.0f} %\nBrake: {:>5.0f} %'.format(ref[0], speeds[0], throttles[0], brakes[0]))
        else:  # adaptive cruise control text
            car_text.set_text('Distance Set Point: {:>5.2f} m\nDistance from Leader: {:>5.2f} m\nSpeed Set Point: {:>5.2f} m/s\nCurrent Speed: {:>5.2f} m/s\nThrottle: {:>5.0f} %\nBrake: {:>5.0f} %'.format(0, position[0] - position[1], 30, speeds[1], throttles[1], brakes[1]))
        return ground, [car.artist for car in cars]

    # create the animation and show it
    ani = animation.FuncAnimation(fig=fig,
                                  func=update,
                                  init_func=initialize,
                                  interval=1000 / render_fps,
                                  frames=frames.size,
                                  repeat=False,
                                  blit=False)
    plt.show()
    return ani
