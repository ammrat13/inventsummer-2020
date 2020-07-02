# This file maintains a Person class, representing a person inside the
# simulation. Perhaps its most important role is to store its own position and
# provide methods to calculate the distances between people.

# Required for postponed type annotations
# See: https://stackoverflow.com/questions/36286894/name-not-defined-in-type-annotation
from __future__ import annotations

# Needed to elegantly keep track of a person's health status
from enum import Enum

# For a more accurate square-root
from math import sqrt


# A separate enum to keep track of the health of a Person
# We keep this outside the Person class for easier access and usage
class Health(Enum):
    HEALTHY = 0


class Person:

    # As I said, it's just a wrapper around these properties ...
    def __init__(self, x: float, y: float, h: Person.Health) -> None:
        self.x = x
        self.y = y
        self.health = h

    # ... and some utility methods to calculate the distances between people in
    #  different ways
    @staticmethod
    def distance_between(p1: Person, p2: Person) -> float:
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        return sqrt(dx**2 + dy**2)

    def distance_to(self, p: Person) -> float:
        return Person.distance_between(self, p)

