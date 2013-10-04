import random

from step import *

class RandomizeStep(BaseStep):

    def __init__(self, scenario):
        BaseStep.__init__(self, scenario)
        self.list_of_numbers = []

    @context("a list containing (\d+) and (\d+)")
    def setup_list(self, *arguments):
        self.list_of_numbers = [int(n) for n in arguments]

    @event("I call the \\'shuffle\\' function on this list")
    def shuffling(self):
        random.shuffle(self.list_of_numbers)

    @postcondition("the list will contain (\d+) items")
    def how_many(self, length):
        length = int(length)
        self.assertEqual(length, len(self.list_of_numbers))
