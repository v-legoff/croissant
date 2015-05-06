from croissant.step import *

class Square(BaseStep):

    @context("a number (\d+)")
    def init(self, number):
        self.number = int(number)

    @event("I square it")
    def square(self):
        self.number = self.number ** 2

    @postcondition("I get (\d+)")
    def result(self, compare):
        self.assertEqual(self.number, int(compare))
