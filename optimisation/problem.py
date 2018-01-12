import requests as req
from time import sleep
import numpy as np
from point import *

MAX_API_ELEMENTS = 100
MAX_API_ELEMENTS_DAILY = 2500
KEY = "AIzaSyATtwrFvepaVpvY0oYYyY_G71Mk97D7yzo"


class Problem:
    """
    Class used to represent a problem, which is a list of patients to visit, a list of nurses and a central office,
    which is the place where all rounds start and end
    """

    def __init__(self, office=None, patients_list=None, nurses_list=None):
        """
        Instanciates a Problem object
        :param office: the central office of the problem
        :param patients_list: the list of patients to be visited
        :param nurses_list: the list of nurses
        """
        if office is None:
            self._office = Office()
        else:
            self._office = office
        if patients_list is None:
            self._patients_list = list()
        else:
            self._patients_list = patients_list
        self._number_of_generated_patients = 0
        self._solutions_list = list()
        self._costs_matrix = None
        self._nurses_list = nurses_list

    def _get_office(self):
        return self._office

    def _set_office(self, office):
        self._office = office
        self._solutions_list = list()

    def _get_patients_list(self):
        return self._patients_list

    def _set_patients_list(self, patients_list):
        self._patients_list = patients_list
        self._solutions_list = list()

    def _get_number_of_generated_patients(self):
        return self._number_of_generated_patients

    def _get_costs_matrix(self):
        return self._costs_matrix

    def _set_costs_matrix(self, costs_matrix):
        self._costs_matrix = costs_matrix

    def _get_savings_matrix(self):
        return self._savings_matrix

    def _set_savings_matrix(self, savings_matrix):
        self._savings_matrix = savings_matrix

    def _get_nurses_list(self):
        return self._nurses_list

    def _set_nurses_list(self, nurses_list):
        self._nurses_list = nurses_list

    def _get_solutions_list(self):
        return self._solutions_list

    office = property(_get_office, _set_office)
    patients_list = property(_get_patients_list, _set_patients_list)
    number_of_generated_patients = property(_get_number_of_generated_patients)
    costs_matrix = property(_get_costs_matrix, _set_costs_matrix)
    savings_matrix = property(_get_savings_matrix, _set_savings_matrix)
    nurses_list = property(_get_nurses_list, _set_nurses_list)
    solutions_list = property(_get_solutions_list)

    def print_patients(self):
        """Prints this problem's patients list"""
        for patient in self._patients_list:
            print(patient)

    def print_office(self):
        """Prints this problem's office"""
        print(self._office)

    def number_of_patients(self):
        """Prints this problem's number of patients"""
        return len(self._patients_list)

    def print_solutions(self):
        """Prints all the found solutions of this problem. If detailed == True, the solutions are printed in detail"""
        for solution in self.solutions_list:
            print("")
            print(solution)

    def generate_random_patients(self, amount=1, x=(48, 49), y=(2, 3), duration_of_care=(600, 1800)):
        """
        Generates random patients for this problem (useful for tests)
        :param amount: the number of patients to be generated
        :param x: tuple representing the range of longitude coordinate within patients should be generated
        :param y: tuple representing the range of latitude coordinate within patients should be generated
        :param duration_of_care: tuple representing the range within patients' duration_of_care attributes
                    should be generated
        """
        for i in range(amount):
            generated_x = ((x[1] - x[0]) * np.random.rand() + x[0])
            generated_y = ((y[1] - y[0]) * np.random.rand() + y[0])
            d = np.random.randint(duration_of_care[0], duration_of_care[1])
            self._number_of_generated_patients += 1
            c = Patient(x=generated_x, y=generated_y, duration_of_care=d)
            self._patients_list.append(c)

    def cost(self, point_a, point_b):
        """
        Returns the cost between point_a and point_b using this problem's cost_matrix. If it has not been initialized
         yet, this method performs the initialization calling maps.googleapis.com
        :param point_a: the first point
        :param point_b: the second point
        :return: the cost (in seconds) of the trip between point_a and point_b
        """
        if self._costs_matrix is None:
            self.calculate_cost_matrix()
        a, b = -1, -1
        for i in range(len(self._patients_list)):
            if point_a is self._patients_list[i]:
                a = i
            if point_b is self._patients_list[i]:
                b = i
        return self._costs_matrix[a + 1][b + 1]

    def query_api(self, start_line, nb_lines, start_column, nb_columns):
        """
        Makes a URL for an API call to fill a rectangle in cost_matrix from start_line to start_line + nb_lines - 1
        and start_column to start_column + nb_columns - 1
        :param start_line: the first line to fill in cost_matrix
        :param nb_lines: the number of lines to fill in cost_matrix
        :param start_column: the first column to fill in cost_matrix
        :param nb_columns: the number of columns to fill in cost_matrix
        :return: a URL to call google maps API to fill the wanted rectangle in cost_matrix
        """
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
        patients_locations = ""
        if start_line == 0:
            if nb_lines > 0:
                patients_locations += str(self._office.address).replace(" ", "%20")
            for i in range(min(nb_lines - 1, len(self._patients_list))):
                patients_locations += "|" + str(self._patients_list[i].address).replace(" ", "%20")
        else:
            for i in range(start_line, min(start_line + nb_lines, len(self._patients_list) + 1)):
                if i > start_line:
                    patients_locations += "|"
                patients_locations += str(self._patients_list[i-1].address).replace(" ", "%20")
        url += patients_locations + "&destinations="
        patients_locations = ""
        if start_column == 0:
            if nb_columns > 0:
                patients_locations += str(self._office.address).replace(" ", "%20")
            for i in range(min(nb_columns - 1, len(self._patients_list))):
                patients_locations += "|" + str(self._patients_list[i].address).replace(" ", "%20")
        else:
            for i in range(start_column, min(start_column + nb_columns, len(self._patients_list) + 1)):
                if i > start_column:
                    patients_locations += "|"
                patients_locations += str(self._patients_list[i-1].address).replace(" ", "%20")
        return url + patients_locations + "&key=" + KEY

    def generate_rectangles(self):
        """
        Divides the cost_matrix into rectangles to call the API (if the matrix is small enough, then only one rectangle
        is generated
        Raises an exception if there are too many patients to call the API
        :return: a list of tuples representing the rectangles to call the API in the following form:
                (start_line, number_of_lines, start_columns, number_of_columns)
        """
        if (self.number_of_patients() + 1)**2 > MAX_API_ELEMENTS_DAILY:
            raise ValueError("Too many patients")
        if self.number_of_patients() == 0:
            return []
        rectangles = []
        height = -1
        for i in range(1, self.number_of_patients() + 2):
            if i * (self.number_of_patients() + 1) > MAX_API_ELEMENTS:
                height = i - 1
                break
        if height == 0:
            raise ValueError("Too many patients")
        if height == -1 and self.number_of_patients() + 1 <= MAX_API_ELEMENTS:
            height = self.number_of_patients() + 1
        number_of_handled_lines = 0
        while number_of_handled_lines < self.number_of_patients()+1:
            rectangles.append((number_of_handled_lines, min(height, self.number_of_patients() + 1 -
                                                           number_of_handled_lines), 0, self.number_of_patients() + 1))
            number_of_handled_lines += height
        return rectangles

    def calculate_cost_matrix(self):
        """
        Calculates the cost_matrix attribute of this problem, calling the googlemaps API as many times as needed
        """
        mat_dim = self.number_of_patients() + 1
        cost_matrix = np.zeros((mat_dim, mat_dim))
        api_calls = self.generate_rectangles()
        for start_line, nb_lines, start_column, nb_columns in api_calls:
            url = self.query_api(start_line, nb_lines, start_column, nb_columns)
            print(url)
            json_matrix = req.get(url).json().get("rows")
            for i in range(nb_lines):
                for j in range(nb_columns):
                    cost_matrix[start_line + i, start_column + j] = json_matrix[i].get("elements")[j]\
                        .get("duration").get("value")
            sleep(1)  # to avoid OVER QUERY LIMIT from API
        self._costs_matrix = cost_matrix
