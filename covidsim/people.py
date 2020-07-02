# This file contains a class for the Population, which is little more than a
# wrapper around a list of Persons. It also provides utility methods for
# instantiating and reading Populations.

# Required for postponed type annotations
# See: https://stackoverflow.com/questions/36286894/name-not-defined-in-type-annotation
from __future__ import annotations

# For generating a random population
import random

# Needed for complex type annotations
from typing import List

# Actually import the Person class
from person import Person, Health


class Population:

    # We have an initializer that takes in a list ...
    def __init__(self, p: List[Person]) -> None:
        self.people = p

    # ... but we also have a utility method to generate a population of a size
    @staticmethod
    def random(
    size: int,
    min_x: float =   0.0, min_y: float =   0.0,
    max_x: float = 100.0, max_y: float = 100.0  ) -> Population:
        return Population( [ person.Person(
            x = random.uniform(min_x, max_x),
            y = random.uniform(min_y, max_y),
            h = Health.HEALTHY
        ) for _ in range(size) ] )

