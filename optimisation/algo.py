import numpy as np
import requests as req

key = "AIzaSyATtwrFvepaVpvY0oYYyY_G71Mk97D7yzo"
MAX_API_ELEMENTS = 100


class Nurse:
    """
    Class used to represent a nurse with his/her start time (in seconds from midnight) and availability (in seconds
    """

    def __init__(self, pk, start_time=0, availability=0):
        """
        Instanciates a Nurse object
        :param pk: the nurse's id
        :param start_time: the start time of availability in seconds from midnight
        :param availability: the availability duration (in seconds) of this nurse
        """
        self.pk = pk
        self.start_time = start_time
        self.availability = availability

    def __str__(self):
        """
        Converts this nurse into a string
        :return: a string representing this nurse
        """
        return "Nurse : pk = {}, availability = {}, start_time = {}".format(self.pk, self.availability, self.start_time)


class Point:
    """
    Class used to represent a point on the map, given its address or latitude/longitude
    """

    def __init__(self, address=None, x=0., y=0., identifier=""):
        """
        Instanciates a Point object. If no address is specified, the address is x,y
        :param identifier: a string identifier for this point
        :param address: a string which represents the address of the point
        :param x: the x coordinate (longitude) of this point
        :param y: the y coordinate (latitude) of this point
        """
        self.identifier = identifier
        if address is None:
            self.address = str(x) + "," + str(y)
        else:
            self.address = address

    def cost(self, other_point, problem):
        """
        Returns the cost (duration) of the trip between self and other_point
        :param other_point: the other point to compute the cost from self
        :param problem: the associated problem, to use its cost_matrix attribute
        :return: the cost between self and other_point
        """
        return problem.cost(self, other_point)

    def __str__(self):
        """
        Converts this point into a string
        :return: a string representing this point
        """
        return "identifier : {}, address : {}".format(self.identifier, self.address)


class Patient(Point):
    """
    Class that iherits from Point, representing a patient on the map
    """

    def __init__(self, address=None, x=0., y=0., identifier="", duration_of_care=0, pk=-1,
                 must_be_visited_exactly_at=-1):
        """
        Instanciates a Patient object. If no address is specified, the address is x,y
        :param address: a string which represents the address of the patient
        :param x: the x coordinate (longitude) of this patient
        :param y: the y coordinate (latitude) of this patient
        :param identifier: a string identifier for this patient
        :param duration_of_care: the duration of the care in seconds
        :param pk: the id of the patient
        :param must_be_visited_exactly_at: the time (in seconds from midnight) when the patient should be exactly
                    visited (-1 if no constraint)
        """
        Point.__init__(self, address=address, x=x, y=y, identifier=identifier)
        self.duration_of_care = duration_of_care
        self.pk = pk
        self.must_be_visited_exactly_at = must_be_visited_exactly_at

    def __str__(self):
        """
        Converts this patient into a string
        :return: a string representing this patient
        """
        result = "identifier : {}, address : {}, duration of care : {}".format(self.identifier, self.address,
                                                                               self.duration_of_care)
        if self.must_be_visited_exactly_at != -1:
            result += ", must be exactly visited at : {}".format(self.must_be_visited_exactly_at)
        return result


class Office(Point):
    """
    Class that inherits from Point, used to represent the central office of the service,
     where all nurses start their rounds from
    """

    def __init__(self, address=None, x=0., y=0., identifier=""):
        """
        Instanciates an Office object. If no address is specified, the address is x,y
        :param identifier: a string identifier for this point
        :param address: a string which represents the address of the office
        :param x: the x coordinate (longitude) of this point
        :param y: the y coordinate (latitude) of this point
        """
        Point.__init__(self, address=address, x=x, y=y, identifier=identifier)


class Round:
    """
    Class used to represent a round for a nurse (starting from and ending at the office, with a list of visited patients
    """

    def __init__(self, patients_list=None, problem=None, nurse=None):
        """
        Instanciates a Round object
        :param patients_list: the list of patients to visit during this round
        :param problem: the associated problem
        :param nurse: the nurse that performs this round
        """
        if patients_list is None:
            self._patients_list = list()
        else:
            self._patients_list = patients_list
        if problem is None:
            self._office = Office()
        else:
            self._office = problem.office
        self._nurse = nurse
        self._problem = problem
        self._total_savings = 0.
        self._total_cost = 0.
        self.update()

    def __str__(self):
        """
        Converts this Round object to a string
        :return: a string representing this round
        """
        result = "Printing round properties :\n"
        result += "Office :\n"
        result += str(self._office) + "\n"
        result += str(self._nurse) + "\n"
        result += "Patients list : ({} patient(s))".format(len(self._patients_list)) + "\n"
        for i in range(len(self._patients_list)):
            patient = self._patients_list[i]
            if i == 0:
                last_point = self._office
            else:
                last_point = self._patients_list[i-1]
            result += "cost of trip : {}".format(self._problem.cost(last_point, patient)) + "\n"
            result += str(patient) + ", visited at {}".format(self.time_when_patient_visited(patient, self._problem)) \
                + "\n"
        result += "cost of trip : {}".format(self._problem.cost(self._patients_list[-1], self._office)) + "\n"
        result += "Round properties :" + "\n"
        result += "Total cost = {}, total savings = {}".format(self._total_cost, self._total_savings) + "\n"
        return result

    def _get_office(self):
        return self._office

    def _set_office(self, office):
        self._office = office
        self.calculate_total_savings()
        self.calculate_total_cost()

    def _get_patients_list(self):
        return self._patients_list

    def _set_patients_list(self, patients_list):
        self._patients_list = patients_list
        self.calculate_total_savings()
        self.calculate_total_cost()

    def _get_problem(self):
        return self._problem

    def _get_total_savings(self):
        return self._total_savings

    def _get_total_cost(self):
        return self._total_cost

    def _get_nurse(self):
        return self._nurse

    def _set_nurse(self, nurse):
        self._nurse = nurse

    office = property(_get_office, _set_office)
    patients_list = property(_get_patients_list, _set_patients_list)
    total_savings = property(_get_total_savings)
    total_cost = property(_get_total_cost)
    problem = property(_get_problem)
    nurse = property(_get_nurse, _set_nurse)

    def print_patients_list(self):
        """Prints this round's patients list to the console"""
        print("Patients list : ({} patient(s))".format(len(self._patients_list)))
        for patient in self._patients_list:
            print(patient)

    def print_office(self):
        """Prints this round's office to the console"""
        print(self._office)

    def print_nurse(self):
        print(self._nurse)

    def print_round(self):
        """Prints this round to the console"""
        print("Printing round properties :")
        print("Office :")
        self.print_office()
        self.print_nurse()
        self.print_patients_list()
        print("Round properties :")
        print("Total cost = {}, total savings = {}"
              .format(self._total_cost, self._total_savings))

    def calculate_total_savings(self):
        """Updates the _total_savings attribute of this round"""
        naive_total = 0
        for patient in self._patients_list:
            naive_total = naive_total + self._problem.cost(self._office, patient) + patient.duration_of_care \
                          + self._problem.cost(patient, self._office)
        self._total_savings = naive_total - self._total_cost

    def calculate_total_cost(self):
        """Updates the _total_cost attribute of this round"""
        if self.patients_list == list():
            self._total_cost = 0
        else:
            t = self._problem.cost(self._office, self._patients_list[0]) + self._patients_list[0].duration_of_care
            for i in range(len(self._patients_list) - 1):
                t += self._problem.cost(self._patients_list[i], self._patients_list[i + 1]) \
                     + self._patients_list[i + 1].duration_of_care
            t += self._problem.cost(self._patients_list[-1], self._office)
            self._total_cost = t

    def update(self):
        """Updates the _total_savings and _total_cost attributes of this round"""
        self.calculate_total_savings()
        self.calculate_total_cost()

    def can_merge_left(self, other_round, force_common_patient=False):
        """
        Returns True if other_round can be merged to the left of the current round, False otherwise.
        If force_common_patient is True then this method returns False if the two rounds don't have a common
        patient at their border.
        :param other_round: the other round that we want to merge with self
        :param force_common_patient: if set to True, forces both rounds to have a common patient at their borders
        :return: True if other_round can be merged to the left of the current round, False otherwise
        """
        if force_common_patient and self.patients_list[0] != other_round.patients_list[-1]:
            return False
        for k in range(len(self.patients_list)):
            if k == 0:
                if self.patients_list[k] in other_round.patients_list[:(len(other_round.patients_list) - 1)]:
                    return False
            else:
                if self.patients_list[k] in other_round.patients_list:
                    return False
        return True

    def can_merge_right(self, other_round, force_common_patient=False):
        """
        Returns True if other_round can be merged to the right of the current round, False otherwise.
        If force_common_patient is True then this method returns False if the two rounds don't have a common
        patient at their border.
        :param other_round: the other round that we want to merge with self
        :param force_common_patient: if set to True, forces both rounds to have a common patient at their borders
        :return: True if other_round can be merged to the right of the current round, False otherwise
        """
        if force_common_patient and self.patients_list[-1] != other_round.patients_list[0]:
            return False
        for k in range(len(self.patients_list)):
            if k == (len(self.patients_list) - 1):
                if self.patients_list[k] in other_round.patients_list[1:]:
                    return False
            else:
                if self.patients_list[k] in other_round.patients_list:
                    return False
        return True

    def can_merge(self, other_round, force_common_patient=False):
        """
        Returns a tuple of booleans, which are respectively the results of can_merge_left and can_merge_right
        calls
        :param other_round: the other round that we want to merge with self
        :param force_common_patient: if set to True, forces both rounds to have a common patient at their borders
        :return: a tuple of booleans, which are respectively the results of can_merge_left and can_merge_right
        calls
        """
        left = self.can_merge_left(other_round, force_common_patient)
        right = self.can_merge_right(other_round, force_common_patient)
        return left, right

    def merge_left(self, other_round, update=True):
        """
        Merges other_round to the left of this round
        :param other_round: the other round that we want to merge with self
        :param update: if set to True, a complete update of self is performed
        """
        pl = other_round.patients_list[:]
        if len(self._patients_list) != 0:
            if pl != [] and pl[-1] == self._patients_list[0]:
                pl = pl + self._patients_list[1:]
            else:
                pl = pl + self._patients_list
        self._patients_list = pl
        if not update:
            self.calculate_total_cost()
        else:
            self.update()

    def merge_right(self, other_round, update=True):
        """
        Merges other_round to the right of this round
        :param other_round: the other round that we want to merge with self
        :param update: if set to True, a complete update of self is performed
        """
        pl = self._patients_list[:]
        if len(other_round.patients_list) != 0:
            if pl != [] and pl[-1] == other_round.patients_list[0]:
                pl = pl + other_round.patients_list[1:]
            else:
                pl = pl + other_round.patients_list
        self._patients_list = pl
        if not update:
            self.calculate_total_cost()
        else:
            self.update()

    def time_when_patient_visited(self, patient_to_visit, problem):
        """
        Computes the time when patient_to_visit (that should be in this round) is visited.
        :param patient_to_visit: the patient
        :param problem: the associated problem
        :return: the time (in seconds from midnight) when the patient is visited
        """
        time = self._nurse.start_time
        if patient_to_visit in self._patients_list:
            time += problem.cost(problem.office, self._patients_list[0])
            for i in range(len(self._patients_list)):
                patient = self._patients_list[i]
                next_patient = None
                if i < len(self._patients_list) - 1:
                    next_patient = self._patients_list[i+1]
                if patient.must_be_visited_exactly_at != -1:
                    time = patient.must_be_visited_exactly_at
                if patient is patient_to_visit:
                    return time
                time += patient.duration_of_care + problem.cost(patient, next_patient)
        return -1

    def can_be_assigned_to(self, nurse, problem):
        """
        Checks if a round can be assigned to a nurse without violating the precise visit time and availability
        constraints
        :param nurse: the nurse we want to assign th round to
        :param problem: the associated problem
        :return: True iff this round can be assigned to a nurse without violating the precise visit time constraints
        """
        time = nurse.start_time + problem.cost(self.office, self.patients_list[0])
        for i in range(len(self._patients_list)-1):
            patient = self._patients_list[i]
            next_patient = self._patients_list[i+1]
            if patient.must_be_visited_exactly_at != -1 and patient.must_be_visited_exactly_at < time:
                return False
            if patient.must_be_visited_exactly_at != -1:
                time = patient.must_be_visited_exactly_at
            else:
                time += patient.duration_of_care + problem.cost(patient, next_patient)
        if self._patients_list[-1].must_be_visited_exactly_at != -1 \
                and self._patients_list[-1].must_be_visited_exactly_at < time:
            return False
        time += self._patients_list[-1].duration_of_care + problem.cost(self._patients_list[-1], problem.office)
        return time <= nurse.start_time + nurse.availability


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

    def __str__(self):
        """
        Converts this object to a string
        :return: a string representing this object
        """
        for rnd in self._rounds_list:
            rnd.update()
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
        self.calculate_total_savings(True)

    def _get_total_savings(self):
        return self._total_savings

    def _get_total_cost(self):
        return self._total_cost

    rounds_list = property(_get_rounds_list, _set_rounds_list)
    total_savings = property(_get_total_savings)
    total_cost = property(_get_total_cost)

    def calculate_total_savings(self, recalculate_for_rounds=False):
        """
        Updates the _total_savings attribute
        :param recalculate_for_rounds: if set to True, recalculates the total_savings attribute for each rnd
        """
        if recalculate_for_rounds:
            for rnd in self._rounds_list:
                rnd.calculate_total_savings()
        self._total_savings = sum([d.total_savings for d in self._rounds_list])

    def calculate_total_cost(self):
        """Updates the _total_cost attribute"""
        self._total_cost = sum([rnd.total_cost for rnd in self.rounds_list])


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
        self.solutions_list = list()
        self._costs_matrix = None
        self._savings_matrix = None
        self._nurses_list = nurses_list
        self._availability_of_nurses = sorted([nurse.availability for nurse in self._nurses_list])

    def _get_office(self):
        return self._office

    def _set_office(self, office):
        self._office = office
        self.solutions_list = list()

    def _get_patients_list(self):
        return self._patients_list

    def _set_patients_list(self, patients_list):
        self._patients_list = patients_list
        self.solutions_list = list()

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

    office = property(_get_office, _set_office)
    patients_list = property(_get_patients_list, _set_patients_list)
    number_of_generated_patients = property(_get_number_of_generated_patients)
    costs_matrix = property(_get_costs_matrix, _set_costs_matrix)
    savings_matrix = property(_get_savings_matrix, _set_savings_matrix)
    nurses_list = property(_get_nurses_list, _set_nurses_list)

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

    def remove_solution_index(self, index):
        """
        "Removes a solution with specified index from the solutions list
        :param index: the index of the solution to remove
        """
        del self.solutions_list[index]

    def remove_solution_named(self, name):
        """
        Removes a solution with specified name from the solutions list
        :param name: the name of the solution to remove
        """
        for i, solution in enumerate(self.solutions_list):
            if solution["Name"] == name:
                del self.solutions_list[i]
                break

    def clear_solutions(self):
        """Removes all solutions from the solutions list"""
        self.solutions_list.clear()

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
            d = np.random.random_integers(duration_of_care[0], duration_of_care[1])
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
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
        patients_locations = ""
        if start_line == 0:
            patients_locations += str(self._office.address)
            for i in range(1, nb_lines - 1):
                patients_locations += "|" + str(self._patients_list[i].address)
        else:
            for i in range(start_line, start_line + nb_lines):
                patients_locations += "|" + str(self._patients_list[i].address)
        url += patients_locations + "&destinations="
        patients_locations = ""
        if start_column == 0:
            patients_locations += str(self._office.address)
            for i in range(1, nb_columns - 1):
                patients_locations += "|" + str(self._patients_list[i].address)
        else:
            for i in range(start_column, start_column + nb_columns):
                patients_locations += "|" + str(self._patients_list[i].address)
        return url + patients_locations + "&key=" + key

    def generate_api_calls(self):
        api_calls = []
        height = -1
        for i in range(1, self.number_of_patients() + 2):
            if i * (self.number_of_patients() + 1) > MAX_API_ELEMENTS:
                height = i - 1
        if height == -1:
            height = self.number_of_patients() + 1
        number_of_handled_lines = 0
        while number_of_handled_lines < self.number_of_patients()+1:
            api_calls.append((number_of_handled_lines, min(height, self.number_of_patients() + 1 -
                                                           number_of_handled_lines), 0, self.number_of_patients() + 1))
        return api_calls

    def calculate_cost_matrix(self):
        """This method calculates the cost_matrix attribute of this problem, calling maps.googleapis.com"""
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
        patients_locations = str(self._office.address)
        for patient in self.patients_list:
            patients_locations += "|" + str(patient.address)
        url += patients_locations + "&destinations=" + patients_locations + "&key=" + key
        print(url)
        json_matrix = req.get(url).json().get("rows")
        mat_dim = self.number_of_patients() + 1
        cost_matrix = np.zeros((mat_dim, mat_dim))
        for i in range(0, mat_dim):
            for j in range(0, mat_dim):
                cost_matrix[i, j] = json_matrix[i].get("elements")[j].get("duration").get("value")
        self.costs_matrix = cost_matrix

    def _calculate_cost_matrix(self):
        mat_dim = self.number_of_patients() + 1
        cost_matrix = np.zeros((mat_dim, mat_dim))
        api_calls = self.generate_api_calls()
        for start_line, nb_lines, start_column, nb_columns in api_calls:
            json_matrix = req.get(self.query_api(start_line, nb_lines, start_column, nb_columns)).json().get("rows")
            for i in range(start_line, start_line + nb_lines):
                for j in range(start_column, start_column + nb_columns):
                    cost_matrix[i, j] = json_matrix[i].get("elements")[j].get("duration").get("value")
        self._costs_matrix = cost_matrix

    def calculate_savings_matrix(self):
        """This method calculates the cost_matrix and savings_matrix attribute of this problem"""
        mat_dim = self.number_of_patients()
        savings_matrix = np.zeros((mat_dim, mat_dim))
        self.calculate_cost_matrix()
        cost_matrix = self.costs_matrix
        for i in range(mat_dim):
            for j in range(mat_dim):
                if i != j:
                    savings_matrix[i, j] = cost_matrix[i + 1, 0] + cost_matrix[0, j + 1] - cost_matrix[i + 1, j + 1]
        self.savings_matrix = savings_matrix


class Solver:
    """Class used to solve a specific problem with Clarke & Wright algorithm,
    with either sequential or parallel version"""

    def __init__(self, problem):
        """
        Instanciates a Solver object
        :param problem: the problem we want to solve
        """
        self._problem = problem
        self._sorted_savings = None
        self._arg_sorted_savings = None

    def _clarke_and_wright_init(self):
        """Initializes the Clarke & Wright algorithm, computing cost_matrix and savings_matrix attributes of
        the problem. Sets the attributes _sorted_savings and _arg_sorted_savings of the solver, which will be
        used later"""
        self._problem.calculate_savings_matrix()
        savings_flat = np.ndarray.flatten(self._problem.savings_matrix)
        arg_sorted_savings = np.argsort(savings_flat)
        sorted_savings = [savings_flat[i] for i in arg_sorted_savings]
        self._sorted_savings = sorted_savings
        self._arg_sorted_savings = arg_sorted_savings

    def _get_patients_pair_from_arg(self, arg_k):
        """
        Returns a tuple (patient_i, patient_j) where both patient_i and patient_j are instance of class Patient,
        and where the savings from patient_i to patient_j is at the (arg_k)th position in sorted_savings
        :param arg_k: the position of potential savings we are looking at
        :return: a tuple (patient_i, patient_j) corresponding to the savings at (arg_k)th position
        """
        number_of_patients = len(self._problem.patients_list)
        patient_i = arg_k // number_of_patients
        patient_j = arg_k % number_of_patients
        return self._problem.patients_list[patient_i], self._problem.patients_list[patient_j]

    @staticmethod
    def _search_rounds_for_patient(patient, rounds_list, left_border=False, interior=False, right_border=False):
        """
        Searches for a specified patient in a list of rounds. The search is performed at the border
        and/or in the interior of the rounds according to the value of the parameters.
        The method returns the instance of class Round where the patient has been found.
        It returns None if the patient has not been found in any of the rounds at the right place.
        :param patient: the patient we are looking for
        :param rounds_list: the list of rounds we are searching the patient in
        :param left_border: If set to True, the patient can be placed at the left border of rounds
        :param interior: If set to True, the patient can be placed in the interior of rounds
        :param right_border: If set to True, the patient can be placed at the right border of rounds
        :return: The round where the patient has been found if it has, None otherwise
        """
        for rnd in rounds_list:
            if interior and len(rnd.patients_list) >= 2:
                if patient in rnd.patients_list[1:-1]:
                    return rnd
            if left_border and len(rnd.patients_list) >= 1:
                if patient == rnd.patients_list[0]:
                    return rnd
            if right_border and len(rnd.patients_list) >= 1:
                if patient == rnd.patients_list[-1]:
                    return rnd
        return None

    @staticmethod
    def _add_round_if_possible(new_round, rounds_list, problem):
        """
        Adds a new round to the rounds list if it is possible
        :param new_round: the new round we want to add
        :param rounds_list: the current rounds list
        :param problem: the associated problem
        """
        busy_nurses = [rnd.nurse for rnd in rounds_list]
        available_nurses = [nurse for nurse in problem.nurses_list if nurse not in busy_nurses]
        for nurse in available_nurses:
            if new_round.can_be_assigned_to(nurse, problem):
                new_round.nurse = nurse
                rounds_list.append(new_round)
                break

    @staticmethod
    def _add_merged_round_if_possible(merged_round, old_round, rounds_list, problem):
        """
        Adds merged_round and removes old_round from rounds_list if possible
        :param merged_round: the merged_round (ie: with a new patient)
        :param old_round: the old round (without the new patient)
        :param rounds_list: the current rounds_list
        :param problem: the associated problem
        """
        busy_nurses = [rnd.nurse for rnd in rounds_list]
        available_nurses = [nurse for nurse in problem.nurses_list if nurse not in busy_nurses]
        if merged_round.can_be_assigned_to(old_round.nurse, problem):
            merged_round.nurse = old_round.nurse
            rounds_list.remove(old_round)
            merged_round.update()
            rounds_list.append(merged_round)
        else:
            for nurse in available_nurses:
                if merged_round.can_be_assigned_to(nurse, problem):
                    merged_round.nurse = nurse
                    rounds_list.remove(old_round)
                    merged_round.update()
                    rounds_list.append(merged_round)

    @staticmethod
    def _merge_rounds_if_possible(left_round, right_round, rounds_list, problem):
        """
        Merges left_round and right_round if possible
        :param left_round: the left round
        :param right_round: the right round
        :param rounds_list: the current rounds list
        :param problem: the associated problem
        """
        busy_nurses = [rnd.nurse for rnd in rounds_list]
        available_nurses = [nurse for nurse in problem.nurses_list if nurse not in busy_nurses]
        merged_round = Round(left_round.patients_list, problem)
        merged_round.merge_right(right_round)
        merged_round.update()
        if merged_round.can_be_assigned_to(left_round.nurse, problem):
            merged_round.nurse = left_round.nurse
            rounds_list.remove(left_round)
            rounds_list.remove(right_round)
            rounds_list.append(merged_round)
        elif merged_round.can_be_assigned_to(right_round.nurse, problem):
            merged_round.nurse = right_round.nurse
            rounds_list.remove(left_round)
            rounds_list.remove(right_round)
            rounds_list.append(merged_round)
        else:
            for nurse in available_nurses:
                if merged_round.can_be_assigned_to(nurse, problem):
                    merged_round.nurse = nurse
                    rounds_list.remove(left_round)
                    rounds_list.remove(right_round)
                    rounds_list.append(merged_round)
                    break

    def _parallel_build_rounds(self):
        """
        Builds a rounds list using the parallel version of Clarke & Wright algorithm
        :return: the rounds list
        """
        rounds_list = []
        n = len(self._sorted_savings)
        for i in range(1, n + 1):
            patient_a, patient_b = self._get_patients_pair_from_arg(self._arg_sorted_savings[n - i])
            patient_a_somewhere = self._search_rounds_for_patient(patient_a, rounds_list, True, True, True)
            patient_b_somewhere = self._search_rounds_for_patient(patient_b, rounds_list, True, True, True)
            patient_a_right = self._search_rounds_for_patient(patient_a, rounds_list, False, False, True)
            patient_b_left = self._search_rounds_for_patient(patient_b, rounds_list, True, False, False)
            if patient_a != patient_b and patient_a_somewhere is None and patient_b_somewhere is None:
                new_round = Round([patient_a, patient_b], problem=self._problem)
                self._add_round_if_possible(new_round, rounds_list, self._problem)
            elif patient_a_right is not None and patient_b_somewhere is None:
                merged_round = Round([patient for patient in patient_a_right.patients_list] + [patient_b],
                                     self._problem)
                self._add_merged_round_if_possible(merged_round, patient_a_right, rounds_list, self._problem)
            elif patient_b_left is not None and patient_a_somewhere is None:
                merged_round = Round([patient_a] + [patient for patient in patient_b_left.patients_list], self._problem)
                self._add_merged_round_if_possible(merged_round, patient_b_left, rounds_list, self._problem)
            elif patient_a_right is not None and patient_b_left is not None:
                if patient_a_right is not patient_b_left and patient_a_right.can_merge_right(patient_b_left):
                    self._merge_rounds_if_possible(patient_a_right, patient_b_left, rounds_list, self._problem)
        return rounds_list

    def _add_single_patient_rounds(self, rounds_list):
        """
        Adds single patient rounds to rounds_list for patients that couldn't be merged in any round
        :param rounds_list: the list of rounds that were built thanks to Clarke & Wright algorithm
        """
        patients_list = self._problem.patients_list
        busy_nurses = [rnd.nurse for rnd in rounds_list]
        available_nurses = [nurse for nurse in self._problem.nurses_list if nurse not in busy_nurses]
        for patient in patients_list:
            visited = False
            for d in rounds_list:
                if patient in d.patients_list:
                    visited = True
                    break
            if not visited:
                new_round = Round([patient], problem=self._problem)
                for nurse in available_nurses:
                    if new_round.can_be_assigned_to(nurse, self._problem):
                        new_round.nurse = nurse
                        rounds_list.append(new_round)
                        available_nurses.remove(nurse)
                        busy_nurses.append(nurse)
                        break

    def compute_clarke_and_wright(self, name=None):
        """
        Computes a complete solution to the problem using the specified version of Clarke & Wright algorithm
        :param name: the given name of the solution (if not specified, it is: version + ' Clarke & Wright'
        :return:
        """
        if name is None:
            name = "Parallel Clarke & Wright"
        self._clarke_and_wright_init()
        rounds_list = self._parallel_build_rounds()
        self._add_single_patient_rounds(rounds_list)
        self._problem.solutions_list.append(Solution(name, rounds_list))
