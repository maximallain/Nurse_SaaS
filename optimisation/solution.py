from round import *


class Solution:
    """
    Class used to represent a solution to a problem, which consists of a list of rounds to be performed by nurses
    """

    def __init__(self, name="Unnamed Solution", rounds_list=None):
        """
        Instanciates a Solution object
        :param name: the name of the solution, default is 'Unnamed solution'
        :param rounds_list: the rounds list of this solution
        """
        if rounds_list is None:
            self._rounds_list = list()
        else:
            self._rounds_list = rounds_list
        self.name = name
        self._total_savings = None
        self._total_cost = None
        self.update()

    def __str__(self):
        """
        Converts this object to a string
        :return: a string representing this object
        """
        self.update()
        string = ""
        string += "Solution name : {}".format(self.name) + "\n"
        string += "number of tours = {}, total cost = {}, total savings = {}".format(len(self._rounds_list),
                                                                                     self._total_cost,
                                                                                     self._total_savings) + "\n"
        for rnd in self._rounds_list:
            string += str(rnd)
        return string

    def _get_rounds_list(self):
        return self._rounds_list

    def _set_rounds_list(self, rounds_list):
        self._rounds_list = rounds_list
        self.calculate_total_cost()
        self.calculate_total_savings()

    def _get_total_savings(self):
        return self._total_savings

    def _get_total_cost(self):
        return self._total_cost

    rounds_list = property(_get_rounds_list, _set_rounds_list)
    total_savings = property(_get_total_savings)
    total_cost = property(_get_total_cost)

    def calculate_total_cost(self):
        """Updates the _total_cost attribute"""
        self._total_cost = sum([rnd.total_cost for rnd in self.rounds_list])

    def calculate_total_savings(self):
        """Updates the _total_savings attribute. A complete update is performed for all rounds in this solution"""
        for rnd in self._rounds_list:
            rnd.calculate_total_savings()
        self._total_savings = sum([d.total_savings for d in self._rounds_list])

    def update(self):
        """Updates both total_cost and total_savings attributes"""
        self.calculate_total_cost()
        self.calculate_total_savings()
