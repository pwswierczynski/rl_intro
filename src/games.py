"""
In this file we store all games that we want to benchmark on
the reinforcement learning.

We create a common abstract interface, in which all the games can be represented.
"""

import gym

from abc import ABCMeta, abstractmethod


class AbstractGame(metaclass=ABCMeta):
    def __init__(self) -> None:

        self.current_result = 0
        self.state = None

    @abstractmethod
    def make_move(self, *args, **kwargs) -> bool:
        """ Function responsible for changing the state of the game
            according to the chosen action.

            :returns
            Function retuns True if the move was completed and False otherwise.
        """
        pass
