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
        self.current_reward = 0
        self.state = None

    @abstractmethod
    def make_move(self, *args, **kwargs) -> bool:
        """ Function responsible for changing the state of the game
            according to the chosen action.

            :returns
            Function retuns True if the move was completed and False otherwise.
        """
        pass


class GymGame(AbstractGame):
    def __init__(self, game_name: str = "MountainCar-v0") -> None:
        """
        Class serving as a common interface for all games included
        in OpenAI's GYM library. For a complete list of games go to:
        http://gym.openai.com/docs/

        :param game_name: str - name of the chosen game environment to be loaded from
            GYM library.
        """

        super(GymGame, self).__init__()
        self.game_name = game_name
        try:
            self.env = gym.make(self.game_name)
        except gym.error.Error:
            print("Unknown game, try again!")

    def display(self) -> None:
        self.env.render()

    def make_move(self, action, *args, **kwargs) -> bool:
        self.state, self.current_reward, completed, _ = env.step(action)

        return completed

    def close(self) -> None:

        self.env.close()
