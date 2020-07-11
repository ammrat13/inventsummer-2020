# Section 6: Set Up the Simulation
# ================================

# Nice to have type hinting
from __future__ import annotations
from typing import List, Tuple

# Needed for some functions
from math import ceil

# Needed for efficient distance calculation
import numpy as np

# Needed for plotting
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as image
import matplotlib.widgets as widgets


class Simulation:

    # Define constants to keep track of people's health
    # We can't use an enum for this since they can't efficiently be put into
    #  numpy arrays
    Health = np.ubyte
    HEALTHY: Simulation.Health = 0
    INFECTED: Simulation.Health = 1
    RECOVERED: Simulation.Health = 2
    DECEASED: Simulation.Health = 3


    def __init__(
      self,
      pop_size: int = 1000,
      initial_cases: int = 1,
      hospital_beds_ratio: float = .003,
      infection_distance: np.float64 = 2.0,
      infection_time: np.uint64 = 20,
      p_infect: float = 0.3,
      p_recover: float = 0.7,
      map_size: np.float64 = 100.0,
    ) -> None:

        # Simulation starts at time t=0
        self.time: int = 0

        # Keep track of the population size for this simulation
        self.pop_size: int = pop_size
        # Also the other parameters given
        self.map_size: np.float64 = map_size
        self.infection_distance: np.float64 = infection_distance
        self.infection_time: np.uint64 = infection_time
        self.p_infect: float = p_infect
        self.p_recover: float = p_recover
        self.p_die: float = 1 - p_recover
        self.hospital_beds_ratio: float = hospital_beds_ratio

        # Position and health of everyone in the population
        self.positions: np.ndarray = \
            np.random.uniform(
                low=0.0,
                high=self.map_size,
                size=(self.pop_size,2),
            )
        self.healths: np.ndarray = \
            np.full(
                shape=(self.pop_size,),
                fill_value=Simulation.HEALTHY,
                dtype=Simulation.Health,
            )
        self.infected_duration: np.ndarray = \
            np.zeros( shape=(self.pop_size,), dtype=np.uint64 )

        # Note that we don't have to randomly draw from `self.healths`. The
        #  positions are all generated in the same way, and they're all
        #  indistinguishable from each other.
        self.healths[0:initial_cases] = Simulation.INFECTED
        self.infected_duration[0:initial_cases] = 1

        # Keep track of the statistics too
        self.currently_infected: List[int] = []
        self.ever_infected: List[int] = []

        # Create the figure for plotting
        self.fig = plt.figure(figsize=(16,9))
        # Add a grid for layout
        grid = self.fig.add_gridspec(nrows=3, ncols=4)
        # Add the map and statistics
        self.map_ax = self.fig.add_subplot(grid[0:,1:])
        self.stats_ax = self.fig.add_subplot(grid[0,0])
        self.check_ax = self.fig.add_subplot(grid[1,0], frame_on=False)
        # Add labels
        self.stats_ax.set_xlabel('Time')
        self.stats_ax.set_ylabel('Cases')
        # Call for updates
        self.map_ani = \
            animation.FuncAnimation(
                self.fig,
                self.tick_map,
                init_func=self.init_map)
        self.stats_ani = \
            animation.FuncAnimation(
                self.fig,
                self.tick_stats)

        # Check buttons and simulation options
        self.log_scale: bool = False
        self.p_movement: float = 1.0
        self.checks = widgets.CheckButtons(self.check_ax, [
            'Use Log Scale',
            'Total Social Distancing',
            'Partial Social Distancing',
        ])
        self.checks.on_clicked(self.checkbox_handler)


    # Makes everyone take a step in a random direction with a given mean of
    #  step length
    def tick_locations(self, step_mean: np.float64 = 2.0) -> None:
        # Compute our step if we move
        # Note the formula for the standard deviation. Distance travelled is
        #  the square-root of the sum of the squares of two normal random
        #  variables, giving a chi-squared distribution.
        dpos = \
            np.random.normal(
                scale=np.sqrt(step_mean/2),
                size=(self.pop_size,2))
        # We don't want to move everyone
        # Dead people don't move
        # For everyone else, we roll some probability of moving, and don't move
        #  if they miss that roll
        dpos[
            (self.healths == Simulation.DECEASED) | \
            (np.random.binomial(1, self.p_movement, size=(self.pop_size,)) == 0)
        ] = np.array([0,0])
        # Acutally update the positions
        # Make sure we don't step outside the map boundary
        self.positions += dpos
        self.positions = np.clip(self.positions, 0.0, self.map_size)


    # Returns an array of size (self.pop_size,) containing at index i the
    #  number of infected people person i is within self.infection_distance of
    def people_transmitting(self) -> np.ndarray:
        # Compute the distance between everyone
        distVectors: np.ndarray = self.positions - self.positions.reshape((self.pop_size,1,2))
        distMat: np.ndarray = np.sqrt(np.sum(distVectors**2, axis=2))
        # Figure out whether a person can be infected by another. The ijth
        #  entry of this matrix will be true iff person i can be infected by
        #  person j
        possibilityMat: np.ndarray = \
            (distMat <= self.infection_distance) * \
            (self.healths == Simulation.INFECTED) * \
            (self.healths == Simulation.HEALTHY).reshape((self.pop_size,1))
        # Sum up how many we can get infected from
        return np.sum(possibilityMat, axis=1)


    # Updates the health of the healthy people to infected if they are near
    #  someone else who is infected. Also counts how long someone has been
    #  infected and changes them to recovered if enough time has passed.
    def tick_healths(self) -> None:
        # Compute who becomes infected at the current time
        self.healths[np.random.binomial(self.people_transmitting(), self.p_infect) > 0] = Simulation.INFECTED
        # Compute who has been infected for a long time
        self.infected_duration[self.healths == Simulation.INFECTED] += 1
        infection_done = self.infected_duration >= self.infection_time
        # Figure out who lives and who dies
        # Recovery happens with probability `p_recover`
        self.healths[infection_done] = Simulation.DECEASED
        self.healths[np.random.binomial(infection_done, self.p_recover) > 0] = Simulation.RECOVERED
        # If they are recovered or deceased, we don't want to reroll their status
        self.infected_duration[infection_done] = 0


    # Utility function for plotting
    # Take in the vector of healths and output the colors they should be
    def health_colors(self) -> np.ndarray:
        return np.vectorize({
            Simulation.HEALTHY: 'blue',
            Simulation.INFECTED: 'red',
            Simulation.RECOVERED: 'green',
            Simulation.DECEASED: 'black',
        }.get)(self.healths)

    # Functions for initializing and updating the map
    def init_map(self):
        self.map_ax.imshow(
            image.imread('map.png'),
            extent=[0, self.map_size, 0, self.map_size],
            aspect='auto')
        self.scatter = \
            self.map_ax.scatter(
                x=self.positions[:,0],
                y=self.positions[:,1],
                c=self.health_colors())
        return self.scatter
    def tick_map(self, _):
        self.tick_locations()
        self.tick_healths()
        self.scatter.set_facecolor(self.health_colors())
        self.scatter.set_offsets(self.positions)
        return self.scatter

    # Same for the statistics
    def tick_stats(self, _):
        # Compute the statistics
        self.time += 1
        self.currently_infected.append(
            np.count_nonzero(self.healths == Simulation.INFECTED))
        self.ever_infected.append(
            np.count_nonzero(self.healths != Simulation.HEALTHY))
        # Plot them
        self.stats_ax.clear()
        self.stats_ax.axhline(y=self.hospital_beds_ratio * self.pop_size, color='red', linestyle='--')
        self.stats_ax.set_yscale('log' if self.log_scale else 'linear')
        self.stats_ax.plot(range(self.time), self.currently_infected, 'red')
        self.stats_ax.plot(range(self.time), self.ever_infected, 'black')

    # Handler for all our checkbox actions
    def checkbox_handler(self, _) -> None:
        # Get the state of the buttons
        state: Tuple[bool, bool, bool] = self.checks.get_status()
        # Set our model accordingly
        self.log_scale = state[0]
        self.p_movement = 0.0 if state[1] else 0.6 if state[2] else 1.0



if __name__ == '__main__':
    print(f"Seed: {np.random.get_state()}")
    sim = Simulation()
    plt.show()
