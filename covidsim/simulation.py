# Section 6: Set Up the Simulation
# ================================

# Nice to have type hinting
from __future__ import annotations
from typing import List

# Needed for some functions
from math import ceil

# Needed for efficient distance calculation
import numpy as np


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
      pop_size: int,
      initial_cases_prob: float,
      infection_distance: np.float64 = 27.0,
      map_size: np.float64 = 100.0,
    ) -> None:

        # Keep track of the population size for this simulation
        self.pop_size: int = pop_size
        # Also the other parameters given
        self.map_size: np.float64 = map_size
        self.infection_distance: np.float64 = infection_distance

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

        # Note that we don't have to randomly draw from `self.healths`. The
        #  positions are all generated in the same way, and they're all
        #  indistinguishable from each other.
        initial_cases: int = ceil( self.pop_size * initial_cases_prob )
        self.healths[0:initial_cases] = Simulation.INFECTED


    # Makes everyone take a step in a random direction with a given mean of
    #  step length
    def tick_locations(self, step_mean: np.float64 = 2.0) -> None:
        # Move
        self.positions += \
            np.random.normal(
                scale=np.sqrt(step_mean/2),
                size=(self.pop_size,2))
        # Make sure we don't step outside the map boundary
        self.positions = np.clip(self.positions, 0.0, self.map_size)


    # Returns an array of size (self.pop_size,) containing at index i the
    #  number of infected people person i is within self.infection_distance of
    def people_transmitting(self) -> np.ndarray:
        # Compute the distance between everyone
        distVectors = self.positions - self.positions.reshape((self.pop_size,1,2))
        distMat = np.sqrt(np.sum(distVectors**2, axis=2))
        # Figure out whether a person can be infected by another. The ijth
        #  entry of this matrix will be true iff person i can be infected by
        #  person j
        possibilityMat = \
            (distMat <= self.infection_distance) * \
            (self.healths != Simulation.HEALTHY) * \
            (self.healths == Simulation.HEALTHY).reshape((self.pop_size,1))
        # Sum up how many we can get infected from
        return np.sum(possibilityMat, axis=1)


    # Updates the health of the healthy people to infected if they are near
    #  someone else who is infected
    def tick_healths(self):
        self.healths[self.people_transmitting() > 0] = Simulation.INFECTED

